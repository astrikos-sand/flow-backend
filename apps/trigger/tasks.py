from django.shortcuts import get_object_or_404

from celery import shared_task

from apps.common.exceptions import bad_request
from apps.flow_new.serializers import (
    FlowSerializer,
    BaseNodePolymorphicSerializer,
    DependencySerializer,
)
from apps.flow_new.models import Flow, InputNode
from apps.flow_new.runtime.worker import submit_task


@shared_task
def periodic_task(flow_id: str):
    flow = get_object_or_404(Flow, pk=flow_id)
    data = {
        "flow": FlowSerializer(flow).data,
        "nodes": BaseNodePolymorphicSerializer(flow.nodes.all(), many=True).data,
    }
    result = submit_task(data)
    return result


def webhook_task(flow_id: str, inputs: dict):
    flow = get_object_or_404(Flow, pk=flow_id)

    input_node = InputNode.objects.filter(flow=flow)
    if input_node.exists():
        flow_inputs = input_node.first().output_slots
        for flow_input in flow_inputs:
            if flow_input.name not in inputs:
                raise bad_request

    data = {
        "flow": FlowSerializer(flow).data,
        "nodes": BaseNodePolymorphicSerializer(flow.nodes.all(), many=True).data,
        "inputs": inputs,
        "lib": DependencySerializer(flow.lib).data,
    }

    result = submit_task(data)
    return result
