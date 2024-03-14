from django.core.validators import RegexValidator

from rest_framework import serializers

from apps.resource.models import ResourceGroup, ResourcePermission


class ResourceGroupSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(write_only=True)
    path = serializers.ReadOnlyField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ResourceGroup.objects.all(),
        allow_null=True,
        write_only=True,
        required=False,
    )
    name_prefix = serializers.CharField(
        write_only=True,
        required=False,
        validators=[
            RegexValidator(
                r"/", inverse_match=True, message="name prefix can't contain '/'"
            )
        ],
    )

    class Meta:
        model = ResourceGroup
        fields = (
            "id",
            "name",
            "name_prefix",
            "resource_type",
            "path",
            "parent",
            "data",
        )

        extra_kwargs = {"name": {"required": False}}
        read_only_fields = ("id",)

    def validate(self, data: dict):
        name = data.get("name", self.instance.name if self.instance else None)
        name_prefix = data.get("name_prefix", None)
        resource_type = data.get(
            "resource_type", self.instance.resource_type if self.instance else None
        )
        parent = data.get("parent", self.instance.parent if self.instance else None)

        is_partial_update = self.instance is not None and self.partial

        if not is_partial_update:
            # in case of partial update, both can be None or both can be non None
            if name is None and name_prefix is None:
                raise serializers.ValidationError(
                    "either name or name_prefix is required"
                )

            if name is not None and name_prefix is not None:
                raise serializers.ValidationError(
                    "name and name_prefix both can't be defined at the same time"
                )

        matching_resources = (
            ResourceGroup.get_root_nodes().filter(
                name=name, resource_type=resource_type
            )
            if parent is None
            else parent.get_children().filter(name=name, resource_type=resource_type)
        )

        matching_resources.exclude(id=self.instance.id if self.instance else None)

        if matching_resources.exists():
            raise serializers.ValidationError(
                f"Resource with same name and resource type already exists under theis parent ({parent or 'root'}) , try using name prefix"
            )

        return super().validate(data)

    def create(self, validated_data: dict):
        name_prefix = validated_data.pop("name_prefix", None)
        data = validated_data.pop("data", None)
        parent: ResourceGroup = validated_data.pop("parent", None)

        resource_type = validated_data.get("resource_type", None)
        name = validated_data.get("name", None)

        if name is None:
            matching_resource_count = (
                ResourceGroup.get_root_nodes().filter(
                    name__startswith=name_prefix, resource_type=resource_type
                )
                if parent is None
                else parent.get_children().filter(
                    name__startswith=name_prefix, resource_type=resource_type
                )
            ).count()

            name = name_prefix
            if matching_resource_count > 0:
                name = f"{name}-{matching_resource_count}"
            validated_data["name"] = name

        resource = (
            ResourceGroup.add_root(**validated_data)
            if parent is None
            else parent.add_child(**validated_data)
        )
        resource.store_data(data)

        return resource


class ResourcePermissionSerializer(serializers.ModelSerializer):

    permission_path = serializers.ReadOnlyField()

    class Meta:
        model = ResourcePermission
        fields = (
            "id",
            "name",
            "action",
            "method",
            "path",
            "parent_resource",
            "permission_path",
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "name": {"required": False},
            "parent_resource": {"required": False},
        }

    def validate(self, data: dict):
        action = data.get("action", self.instance.action if self.instance else None)
        method = data.get("method", self.instance.method if self.instance else None)
        path = data.get("path", self.instance.path if self.instance else None)
        parent_resource = data.get(
            "parent_resource", self.instance.parent_resource if self.instance else None
        )

        # policies with same path and parent_resource should not exist
        # Optimises checking because many policies can have same path but different parent_resource
        matching_policy = ResourcePermission.objects.filter(
            path=path,
            parent_resource=parent_resource,
            method=method,
            action=action,
        )

        if self.instance:
            matching_policy = matching_policy.exclude(id=self.instance.id)

        if matching_policy.exists():
            raise serializers.ValidationError(
                "Resource permission with same path and parent_resource already exists"
            )

        # policies with same permission path should not exist
        resource_path = path.split("/").pop()
        possible_matching_policy = ResourcePermission.objects.filter(
            path__endswith=f"/{resource_path}", method=method, action=action
        )

        if self.instance:
            possible_matching_policy = possible_matching_policy.exclude(
                id=self.instance.id
            )

        permission_path = f"{parent_resource.path}/{path}" if parent_resource else path
        for policy in possible_matching_policy:
            if policy.permission_path == permission_path:
                raise serializers.ValidationError(
                    "Resource permission with same permission path already exists"
                )

        return super().validate(data)

    def create(self, validated_data: dict):
        return ResourcePermission.objects.create(**validated_data)

    def update(self, instance: ResourcePermission, validated_data: dict):
        instance.name = validated_data.get("name", instance.name)
        instance.action = validated_data.get("action", instance.action)
        instance.method = validated_data.get("method", instance.method)
        instance.path = validated_data.get("path", instance.path)
        instance.parent_resource = validated_data.get(
            "parent_resource", instance.parent_resource
        )
        instance.save()
        return instance
