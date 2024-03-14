from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.iam.models import IAMUser, Role
from apps.iam.serializers import IAMUserSerialzier, RoleSerializer


class IAMUserViewSet(ModelViewSet):
    queryset = IAMUser.objects.all()
    serializer_class = IAMUserSerialzier
    # permission_classes = (IsAuthenticated, IsAdminUser)

    @action(
        detail=False,
        methods=["get", "post", "delete"],
        url_path="permissions",
        url_name="permissions",
    )
    def attach_permissions(self, request):
        pass

    @action(
        detail=False,
        methods=["get", "post", "delete"],
        url_path="roles",
        url_name="roles",
    )
    def attach_roles(self, request):
        pass


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = (IsAuthenticated, IsAdminUser)

    @action(
        detail=False,
        methods=["get", "post", "delete"],
        url_path="permissions",
        url_name="permissions",
    )
    def attach_permissions(self, request):
        pass


router = DefaultRouter()
router.register(r"users", IAMUserViewSet, basename="user")
router.register(r"roles", RoleViewSet, basename="role")
