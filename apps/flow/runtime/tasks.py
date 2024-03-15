from django.db.models import Count, Q, QuerySet

import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from apps.flow.models import (
    FlowFile,
    Connection,
    BaseNode,
)

parameter_map: dict[dict] = {}
lock = Lock()


def execute_node(node):
    # fetch parameters
    inputs = parameter_map.get(node.id, {})

    globals = {}
    children = []

    # if all input parameters exist then execute the node and submit all child not execute node, else return

    if all(param in inputs for param in node.input_slots):
        # execute the node
        outputs = node.execute(globals, inputs)
        print("outputs:", outputs, node)

        # for all output parameters, update the parameter map and submit the child nodes for execution
        source_connections: QuerySet[Connection] = node.source_connections.all()
        for connection in source_connections:
            target_node = connection.target.get_real_instance()
            target_slot = connection.target_slot
            output = outputs.get(connection.source_slot, None)

            with lock:
                parameter_map.setdefault(target_node.id, {}).update(
                    {target_slot: output}
                )

            children.append(target_node)

    return children


def submit_node_task(node, executor):
    future = executor.submit(execute_node, node)

    # raises error when there is any error in execution
    children = future.result()

    for child in children:
        submit_node_task(child, executor)


def execute_flow(flow_file_id: uuid.UUID):
    try:
        flow_file = FlowFile.objects.get(id=flow_file_id)
        nodes = BaseNode.objects.filter(flow_file=flow_file)
        start_nodes = []

        for node in nodes:
            if len(node.input_slots) == 0:
                start_nodes.append(node)

        with ThreadPoolExecutor(10) as executor:

            for node in start_nodes:
                submit_node_task(node, executor)

    except Exception as e:
        print(e)
        return False
