from django.contrib.auth import authenticate, login

from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from apps.iam.models import IAMUser, Role
from apps.iam.serializers import IAMUserSerialzier, RoleSerializer
from apps.common.permission import IsSuperUser


class IAMUserViewSet(ModelViewSet):
    queryset = IAMUser.objects.all()
    serializer_class = IAMUserSerialzier
    permission_classes = (IsSuperUser,)

    @action(
        detail=True,
        methods=["POST"],
    )
    def attach(self, request: Request, pk=None):
        permissions = request.data.get("permissions", [])
        roles = request.data.get("roles", [])
        user = IAMUser.objects.get(pk=pk)

        user.permissions.add(*permissions)
        user.roles.add(*roles)

        return Response(status=status.HTTP_200_OK)

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
    permission_classes = (IsSuperUser,)

    @action(
        detail=False,
        methods=["get", "post", "delete"],
        url_path="permissions",
        url_name="permissions",
    )
    def attach_permissions(self, request):
        pass


class LoginViewSet(ViewSet):
    @action(
        detail=False,
        methods=["post"],
    )
    def login(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        data = IAMUserSerialzier(user).data
        return Response(data, status=status.HTTP_200_OK)


router = DefaultRouter()
router.register(r"users", IAMUserViewSet, basename="user")
router.register(r"roles", RoleViewSet, basename="role")
router.register(r"auth", LoginViewSet, basename="auth")
