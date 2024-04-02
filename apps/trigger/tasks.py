from apps.flow.models import BaseNode
from apps.flow.serializers import BaseNodeSerializer
from apps.flow.runtime.worker import submit_task, save_results, SUBMIT_TASK_TYPE
from celery import shared_task


def create_nodes(node: BaseNode, nodes_list: list):
    nodes_list.append(node)
    for connection in node.source_connections.all():
        target_node = connection.target.get_real_instance()
        create_nodes(target_node, nodes_list)


@shared_task
def periodic_task(node_id: str):
    node = BaseNode.objects.get(id=node_id).get_real_instance()
    nodes_list = []
    delayed_slots = node.delayed_output_slots + [
        slot.get("name") for slot in node.delayed_special_output_slots
    ]
    nodes_list.append(node)
    # only append nodes connected to delayed output slots
    for connection in node.source_connections.all():
        source_slot = connection.source_slot
        if source_slot in delayed_slots:
            create_nodes(connection.target.get_real_instance(), nodes_list)
    nodes_list = list(set(nodes_list))
    nodes_list = BaseNodeSerializer(nodes_list, many=True).data
    response = submit_task(
        nodes=nodes_list, type=SUBMIT_TASK_TYPE.TRIGGERED, trigger_node=node_id
    )
    result = response.get("outputs", {})
    save_results(result)
    return response


def webhook_task(node: BaseNode, data, request):
    nodes_list = []
    node = node.get_real_instance()
    delayed_slots = node.delayed_output_slots + [
        slot.get("name") for slot in node.delayed_special_output_slots
    ]
    nodes_list.append(node)
    # only append nodes connected to delayed output slots
    for connection in node.source_connections.all():
        source_slot = connection.source_slot
        if source_slot in delayed_slots:
            create_nodes(connection.target.get_real_instance(), nodes_list)
    nodes_list = list(set(nodes_list))
    nodes_data = BaseNodeSerializer(
        nodes_list, many=True, context={"request": request}
    ).data
    response = submit_task(
        nodes=nodes_data,
        data=data,
        type=SUBMIT_TASK_TYPE.TRIGGERED,
        trigger_node=node.id,
    )
    result = response.get("outputs", {})
    save_results(result)
    return response
