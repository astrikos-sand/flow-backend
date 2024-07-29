from django.shortcuts import get_object_or_404

from celery import shared_task

from apps.flow_new.serializers import FlowSerializer, BaseNodePolymorphicSerializer
from apps.flow_new.models import Flow
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


def webhook_task(flow_id: str):
    flow = get_object_or_404(Flow, pk=flow_id)
    data = {
        "flow": FlowSerializer(flow).data,
        "nodes": BaseNodePolymorphicSerializer(flow.nodes.all(), many=True).data,
    }
    result = submit_task(data)
    return result
