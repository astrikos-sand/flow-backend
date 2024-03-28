from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.routers import DefaultRouter

from apps.flow.models import BaseNode, BaseNodeClass, FlowFile
from apps.flow.serializers import (
    BaseNodeSerializer,
    BaseNodeClassSerializer,
    FlowFileSerializer,
)
from apps.flow.runtime.worker import submit_task


class BaseNodeViewSet(ModelViewSet):
    queryset = BaseNode.objects.all()
    serializer_class = BaseNodeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class BaseNodeClassViewSet(ModelViewSet):
    queryset = BaseNodeClass.objects.all()
    serializer_class = BaseNodeClassSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class FlowFileViewSet(ModelViewSet):
    queryset = FlowFile.objects.all()
    serializer_class = FlowFileSerializer


class TaskViewSet(ViewSet):

    def create(self, request):
        file_id = request.data.get("file_id", None)
        if file_id is None:
            return Response(
                {"error": "file_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        nodes = BaseNode.objects.filter(flow_file__id=file_id)
        nodes_data = BaseNodeSerializer(
            nodes, many=True, context={"request": request}
        ).data
        try:
            response = submit_task(nodes_data)
        except Exception as e:
            response = {"error": str(e)}
            print({"error": str(e)})
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_200_OK)


router = DefaultRouter()
router.register(r"nodes", BaseNodeViewSet, basename="node")
router.register(r"flows", FlowFileViewSet, basename="flow")
router.register(r"node-classes", BaseNodeClassViewSet, basename="node-class")
router.register(r"tasks", TaskViewSet, basename="task")
