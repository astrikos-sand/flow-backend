import re

from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import IsAuthenticated

from apps.resource.models import ResourceGroup, ResourcePermission
from apps.resource.serializers import (
    ResourceGroupSerializer,
    ResourcePermissionSerializer,
)
from apps.common.permission import IsSuperUser
from apps.resource.utils import get_action


class ResourceViewSet(ModelViewSet):
    serializer_class = ResourceGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ResourceGroup.objects.all()
        permissions = user.get_resource_permissions()

        action = get_action(self.action)
        resource_list = []
        for perm in permissions:
            permission = ResourcePermission.objects.get(pk=perm)
            if (
                permission.method == ResourcePermission.Method.ALLOW
                and permission.action == action
            ):
                path = permission.permission_path
                regex_pattern = re.compile(path)
                all_resources = ResourceGroup.objects.all()
                resources = list(
                    filter(lambda x: regex_pattern.search(x.path), all_resources)
                )
                resource_list.extend(resources)
        return resource_list


class ResourcePermissionViewSet(ModelViewSet):
    queryset = ResourcePermission.objects.all()
    serializer_class = ResourcePermissionSerializer
    permission_classes = (IsSuperUser,)


router = DefaultRouter()
router.register(r"resources", ResourceViewSet, basename="resource")
router.register(r"permissions", ResourcePermissionViewSet, basename="permission")
