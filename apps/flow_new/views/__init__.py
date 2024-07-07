from rest_framework.routers import DefaultRouter

from apps.flow_new.views.tags import *
from apps.flow_new.views.nodes import *

router = DefaultRouter()
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"archives", FileArchiveViewSet)
router.register(r"nodes", BaseNodeViewSet, basename="nodes")
router.register(r"flow", FlowViewSet, basename="flow")
router.register(r"dependency", DependencyViewSet, basename="dependency")
router.register(
    r"function-definitions", FunctionDefinitionViewSet, basename="function-definitions"
)
