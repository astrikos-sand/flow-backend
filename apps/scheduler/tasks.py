from apps.flow.models import BaseNode
from apps.flow.runtime.worker import submit_task, SUBMIT_TASK_TYPE

def create_nodes(node: BaseNode, nodes_list: list):
    nodes_list.append(node)
    for connection in node.source_connections.all():
        target_node = connection.target.get_real_instance()
        create_nodes(target_node, nodes_list)
        
def period_task(node):
    nodes_list = []
    create_nodes(node=node, nodes_list=nodes_list)
    return submit_task(nodes_list=nodes_list, type=SUBMIT_TASK_TYPE.TRIGGERED, trigger_node=node)

def webhook_task(node, data):
    nodes_list = []
    create_nodes(node=node, nodes_list=nodes_list)
    return submit_task(nodes_list=nodes_list, data=data, type=SUBMIT_TASK_TYPE.TRIGGERED, trigger_node=node)