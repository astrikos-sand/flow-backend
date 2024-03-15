from django.db.models import Count, Q, QuerySet

import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from polymorphic.query import PolymorphicQuerySet

from apps.flow.models import FlowFile, DataNode, DynamicNode, Connection, Slot, DynamicNodeClass, BaseNode

parameter_map: dict[dict] = {}
lock = Lock

def execute_node(node, executor):
    # fetch parameters
    inputs = parameter_map.get(node.id, {})
    globals = {}
    
    # if all input parameters exist then execute the node and submit all child not execute node, else return
    if all(param in inputs for param in node.input_slots):
        
        # execute the node
        print('Executing: ', node.id, 'inputs: ', inputs ,'outputs', outputs)
        outputs = node.execute(globals, inputs)
        
        # for all output parameters, update the parameter map and submit the child nodes for execution
        source_connections: QuerySet[Connection] = node.source_connections.all()
        for connection in source_connections:
            target_node = connection.target
            target_slot = connection.target_slot
            output = outputs.get(connection.source_slot, None)
            
            with lock:
                parameter_map.setdefault(target_node.id, {}).update({target_slot: output})
                print('parameter map: ', parameter_map)
            
            executor.submit(execute_node, target_node, executor)
        

def execute_flow(flow_file_id: uuid.UUID):
    try:
        flow_file = FlowFile.objects.get(id=flow_file_id)
        nodes = BaseNode.objects.filter(flow_file=flow_file)
        start_nodes = []
        
        for node in nodes:
            print('nodes: ', node, node.input_slots)
            if len(node.input_slots) == 0:
                start_nodes.append(node)
        
        
        with ThreadPoolExecutor(10) as executor:
            
            for node in start_nodes:
                executor.submit(execute_node, node, executor)
                
    except Exception as e:
        print(e)
        return False
