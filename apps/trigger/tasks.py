from apps.flow.models import BaseNode
from apps.flow.serializers import BaseNodeSerializer
from apps.flow.runtime.worker import submit_task, SUBMIT_TASK_TYPE


def create_nodes(node: BaseNode, nodes_list: list):
    nodes_list.append(node)
    for connection in node.source_connections.all():
        target_node = connection.target.get_real_instance()
        create_nodes(target_node, nodes_list)


def period_task(node, context):
    nodes_list = []
    node = node.get_real_instance()
    create_nodes(node=node, nodes_list=nodes_list)
    nodes_data = BaseNodeSerializer(nodes_list, many=True, context=context).data
    return submit_task(
        nodes=nodes_data, type=SUBMIT_TASK_TYPE.TRIGGERED, trigger_node=node.id
    )


def webhook_task(node, data, request):
    nodes_list = []
    node = node.get_real_instance()
    create_nodes(node=node, nodes_list=nodes_list)
    nodes_data = BaseNodeSerializer(
        nodes_list, many=True, context={"request": request}
    ).data
    return submit_task(
        nodes=nodes_data,
        data=data,
        type=SUBMIT_TASK_TYPE.TRIGGERED,
        trigger_node=node.id,
    )
