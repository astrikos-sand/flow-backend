from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.routers import DefaultRouter
from rest_framework import status
from rest_framework.response import Response

from apps.webhook.models import WebHookEvent
from apps.webhook.serializers import WebHookEventSerializer

from apps.flow.models import BaseNode
from apps.flow.runtime.worker import submit_task


def create_nodes(node: BaseNode, nodes_list: list):
    nodes_list.append(node)
    for connection in node.source_connections.all():
        target_node = connection.target.get_real_instance()
        create_nodes(target_node, nodes_list)


class WebHookEventViewSet(ModelViewSet):
    queryset = WebHookEvent.objects.all()
    serializer_class = WebHookEventSerializer


class WebHookViewSet(ViewSet):

    def create(self, request):
        data = request.get("data", None)
        trigger_id = request.get("event", None)
        trigger = BaseNode.objects.get(id=trigger_id)
        nodes_list = []
        create_nodes(trigger, nodes_list)
        print("nodes_list", nodes_list)
        data = {}
        data.update({trigger_id: {"data": data, "speciality": "WEBHOOK"}})
        print("data", data)
        submit_task(nodes_list, data)
        return Response(request.data, status=status.HTTP_200_OK)


router = DefaultRouter()
router.register(r"webhook-events", WebHookEventViewSet, basename="webhook-event")
router.register(r"webhook", WebHookViewSet, basename="webhook")
