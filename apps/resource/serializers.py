from rest_framework import serializers

from apps.resource.models import ResourceGroup


class ResourceGroupSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()
    path = serializers.ReadOnlyField()

    class Meta:
        model = ResourceGroup
        fields = (
            "name",
            "resource_type",
            "path",
            "data",
        )

    def create(self, validated_data: dict):
        data = validated_data.pop("data", None)
        resource = ResourceGroup.add_root(**validated_data)
        resource.store_data(data)
        return resource
