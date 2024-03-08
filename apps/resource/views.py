from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter

from apps.resource.models import ResourceGroup
from apps.resource.serializers import ResourceGroupSerializer


class ResourceViewSet(ModelViewSet):
    queryset = ResourceGroup.objects.all()
    serializer_class = ResourceGroupSerializer


router = DefaultRouter()
router.register(r"resources", ResourceViewSet, basename="resource")
