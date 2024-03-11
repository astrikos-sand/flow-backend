from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from rest_framework import serializers, validators

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
        name = data.get("name", None)
        name_prefix = data.get("name_prefix", None)
        resource_type = data.get("resource_type", None)
        parent = data.get("parent", None)

        if name is None and name_prefix is None:
            raise ValidationError("either name or name_prefix is required")

        if name is not None and name_prefix is not None:
            raise ValidationError(
                "name and name_prefix both can't be defined at the same time"
            )

        matching_resource_count = (
            ResourceGroup.get_root_nodes().filter(
                name=name, resource_type=resource_type
            )
            if parent is None
            else parent.get_children().filter(name=name, resource_type=resource_type)
        )

        if matching_resource_count.count() > 0:
            raise ValidationError(
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
