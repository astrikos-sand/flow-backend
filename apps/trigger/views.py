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

    @action(detail=True, methods=["post"], url_path="trigger", url_name="trigger")
    def trigger(self, request, pk=None):
        hook: WebHookTrigger = self.get_object()
        data = {"data": request.data}
        try:
            result = webhook_task(node=hook.node, data=data, request=request)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)


class PeriodicTriggerViewSet(ModelViewSet):
    queryset = PeriodicTrigger.objects.all()
    serializer_class = PeriodicTriggerSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.task.delete()
        print("deleted task, instance will be automatcally deleted by cascade")
        return Response(status=status.HTTP_204_NO_CONTENT)


router = DefaultRouter()
router.register(r"webhook-triggers", WebHookTriggerViewSet, basename="webhook-trigger")
router.register(
    r"periodic-triggers", PeriodicTriggerViewSet, basename="periodic-trigger"
)
