from rest_framework.routers import DefaultRouter

from apps.flow.views.tags import *
from apps.flow.views.nodes import *
from apps.flow.views.utils import *

router = DefaultRouter()
router.register(r"archives", FileArchiveViewSet)
router.register(r"nodes", BaseNodeViewSet, basename="nodes")
router.register(r"flow", FlowViewSet, basename="flow")
router.register(r"env", DependencyViewSet, basename="dependency")
router.register(
    r"function-definitions", FunctionDefinitionViewSet, basename="function-definitions"
)
router.register(r"connections", ConnectionViewSet, basename="connections")
router.register(r"fields", DynamicFieldsViewSet, basename="dynamic-fields")
router.register(r"data-transfer", DataTransferManager, basename="data-transfer")
