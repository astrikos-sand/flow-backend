from django.core.exceptions import ValidationError

from rest_framework import serializers

from apps.resource.models import ResourceGroup


class ResourceGroupSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(write_only=True)
    path = serializers.ReadOnlyField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ResourceGroup.objects.all(),
        allow_null=True,
        write_only=True,
        required=False,
    )
    name_prefix = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ResourceGroup
        fields = ("name", "resource_type", "path", "parent", "data", "name_prefix")
        extra_kwargs = {
            "name": {"required": False},
        }

    def validate(self, data: dict):
        name = data.get("name", None)
        name_prefix = data.pop("name_prefix", None)  # remove name_prefix from data
        resource_type = data.get("resource_type", None)
        parent = data.get("parent", None)

        # raises validation error if object to be created can't have a unique path
        data["name"] = ResourceGroup.validate(
            name=name,
            name_prefix=name_prefix,
            resource_type=resource_type,
            parent=parent,
        )
        return super().validate(data)

    def create(self, validated_data: dict):
        data = validated_data.pop("data", None)
        parent = validated_data.pop("parent", None)
        resource = (
            ResourceGroup.add_root(**validated_data)
            if parent is None
            else parent.add_child(**validated_data)
        )
        resource.store_data(data)
        return resource
