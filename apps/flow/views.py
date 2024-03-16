from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter

from apps.flow.models import BaseNode, BaseNodeClass, FlowFile
from apps.flow.serializers import (
    BaseNodeSerializer,
    BaseNodeClassSerializer,
    FlowFileSerializer,
)

# Create your views here.


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


router = DefaultRouter()
router.register(r"nodes", BaseNodeViewSet, basename="node")
router.register(r"flows", FlowFileViewSet, basename="flow")
router.register(r"node-classes", BaseNodeClassViewSet, basename="node-class")
