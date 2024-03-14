from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.resource.models import ResourceGroup, ResourcePermission
from apps.resource.serializers import (
    ResourceGroupSerializer,
    ResourcePermissionSerializer,
)


class ResourceViewSet(ModelViewSet):
    queryset = ResourceGroup.objects.all()
    serializer_class = ResourceGroupSerializer
    # permission_classes = (IsAuthenticated, IsAdminUser)


class ResourcePermissionViewSet(ModelViewSet):
    queryset = ResourcePermission.objects.all()
    serializer_class = ResourcePermissionSerializer
    # permission_classes = (IsAuthenticated, IsAdminUser)


router = DefaultRouter()
router.register(r"resources", ResourceViewSet, basename="resource")
router.register(r"permissions", ResourcePermissionViewSet, basename="permission")
