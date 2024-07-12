from rest_framework import serializers

from apps.flow_new.models import FunctionField, FunctionDefinition, FunctionNode, Slot
from apps.flow_new.serializers.nodes import BaseNodeSerializer, SlotSerializer


class FunctionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionField
        exclude = (
            "definition",
            "created_at",
            "updated_at",
        )


class FunctionDefinitionSerializer(serializers.ModelSerializer):
    fields = FunctionFieldSerializer(many=True, write_only=True)

    class Meta:
        model = FunctionDefinition
        exclude = (
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        fields = validated_data.pop("fields")
        definition = FunctionDefinition.objects.create(**validated_data)
        for field in fields:
            FunctionField.objects.create(definition=definition, **field)
        return definition


class FunctionNodeSerializer(BaseNodeSerializer):
    class Meta(BaseNodeSerializer.Meta):
        model = FunctionNode

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["definition"] = FunctionDefinitionSerializer(instance.definition).data
        return data

    def create(self, validated_data):
        definition = validated_data.pop("definition")
        function_node = FunctionNode.objects.create(
            definition=definition, **validated_data
        )
        serializer = FunctionFieldSerializer(definition.fields, many=True)
        fields = serializer.data

        for field in fields:
            data = {
                "name": field["name"],
                "attachment_type": field["attachment_type"],
                "value_type": field["value_type"],
            }
            Slot.objects.create(node=function_node, **data)

        return function_node
