from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action

from apps.scheduler.tasks import webhook_task
from apps.scheduler.models import WebHookScheduler, PeriodicScheduler
from apps.scheduler.serializers import WebHookScheduleSerializer, PeriodicScheduleSerializer

class WebHookSchedulerViewSet(ModelViewSet):
    queryset = WebHookScheduler.objects.all()
    serializer_class = WebHookScheduleSerializer

    @action(detail=True, methods=["post"], url_path="trigger", url_name="trigger")
    def trigger(self, request, pk=None):
        hook: WebHookScheduler = self.get_object()
        data = request.data.get('data', None)
        try:
            result = webhook_task(node=hook.node, data=data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)

class PeriodicScheduleViewSet(ModelViewSet):
    queryset = PeriodicScheduler.objects.all()
    serializer_class = PeriodicScheduleSerializer

    
    
router = DefaultRouter()
router.register(r"webhook-schedulers", WebHookSchedulerViewSet, basename="webhook-scheduler")
router.register(r'periodic-schedulers', PeriodicScheduleViewSet, basename='periodic-scheduler')