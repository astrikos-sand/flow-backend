from django.db.models import Count, Q

import uuid
from concurrent.futures import ThreadPoolExecutor

from apps.flow.models import FlowFile, Node, DataNodeClass, DynamicNodeClass, Connections, Parameter

parameter_map = {}

def execute_node(node: Node):
    pass

def execute_flow(flow_file_id: uuid.UUID):
    try:
        flow_file = FlowFile.objects.get(id=flow_file_id)
        
        start_data_classes = DataNodeClass.objects.all()
        start_dynamic_classes= DynamicNodeClass.objects.annotate(num_inputs=Count('parameters', filter=(Q(parameters__behaviour=Parameter.BEHAVIOUR.INPUT)))).filter(num_inputs=0)

        start_data_nodes = Node.objects.filter(flow_file=flow_file, node_class__in=start_data_classes)
        start_dynamic_nodes = Node.objects.filter(flow_file=flow_file, node_class__in=start_dynamic_classes)
        
        print("start_data_nodes",start_data_nodes, flush=True)
        print("start_dynamic_nodes",start_dynamic_nodes, flush=True)
        
        with ThreadPoolExecutor(10) as executor:
            for node in start_data_nodes:
                executor.submit(execute_node, node)
            
            for node in start_dynamic_nodes:
                executor.submit(execute_node, node)

    except Exception as e:
        print(e)
        return
