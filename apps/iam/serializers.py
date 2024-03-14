from rest_framework import serializers

from apps.iam.models import IAMUser, Role
from apps.resource.models import ResourcePermission
from apps.resource.serializers import ResourcePermissionSerializer

from apps.common.fields import NestedPrimaryKeyRelatedField


class RoleSerializer(serializers.ModelSerializer):
    permissions = NestedPrimaryKeyRelatedField(
        serializer=ResourcePermissionSerializer,
        queryset=ResourcePermission.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Role
        fields = ("id", "name", "permissions")

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        role = Role.objects.create(**validated_data)
        role.permissions.set(permissions)
        return role

    def update(self, instance, validated_data):
        instance.name = validated_data.pop("name", instance.name)
        instance.save()

        instance.permissions.set(
            validated_data.pop("permissions", instance.permissions.all())
        )

        return instance


class IAMUserSerialzier(serializers.ModelSerializer):
    permissions = NestedPrimaryKeyRelatedField(
        serializer=ResourcePermissionSerializer,
        queryset=ResourcePermission.objects.all(),
        many=True,
        required=False,
    )
    roles = NestedPrimaryKeyRelatedField(
        serializer=RoleSerializer,
        queryset=Role.objects.all(),
        many=True,
        required=False,
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = IAMUser
        fields = (
            "id",
            "username",
            "password",
            "is_active",
            "is_superuser",
            "permissions",
            "roles",
        )

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        roles = validated_data.pop("roles", [])
        user = IAMUser.objects.create_user(**validated_data)
        user.permissions.set(permissions)
        user.roles.set(roles)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.pop("username", instance.username)
        instance.is_active = validated_data.pop("is_active", instance.is_active)
        instance.is_superuser = validated_data.pop(
            "is_superuser", instance.is_superuser
        )

        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        instance.save()

        instance.permissions.set(
            validated_data.pop("permissions", instance.permissions.all())
        )
        instance.roles.set(validated_data.pop("roles", instance.roles.all()))

        return instance
