from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action

from apps.trigger.tasks import webhook_task
from apps.trigger.models import WebHookTrigger, PeriodicTrigger
from apps.trigger.serializers import (
    WebHookTriggerSerializer,
    PeriodicTriggerSerializer,
)


class WebHookTriggerViewSet(ModelViewSet):
    queryset = WebHookTrigger.objects.all()
    serializer_class = WebHookTriggerSerializer

    @action(detail=True, methods=["post"])
    def execute(self, request, pk: str):
        hook: WebHookTrigger = self.get_object()
        inputs = request.data.get("inputs", {})
        result = webhook_task(flow_id=str(hook.target.id), inputs=inputs)
        return Response(result, status=status.HTTP_200_OK)


class PeriodicTriggerViewSet(ModelViewSet):
    queryset = PeriodicTrigger.objects.all()
    serializer_class = PeriodicTriggerSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


router = DefaultRouter()
router.register(r"webhook", WebHookTriggerViewSet, basename="webhook-trigger")
router.register(r"periodic", PeriodicTriggerViewSet, basename="periodic-trigger")
