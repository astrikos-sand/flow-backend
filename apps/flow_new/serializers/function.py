from rest_framework import serializers

from apps.flow_new.models import FunctionField, FunctionDefinition, FunctionNode, Slot
from apps.flow_new.serializers.nodes import BaseNodeSerializer, SlotSerializer


class FunctionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionField
        exclude = ("definition",)


class FunctionDefinitionSerializer(serializers.ModelSerializer):
    fields = FunctionFieldSerializer(many=True)

    class Meta:
        model = FunctionDefinition
        fields = "__all__"

    def create(self, validated_data):
        fields = validated_data.pop("fields")
        definition = FunctionDefinition.objects.create(**validated_data)
        for field in fields:
            FunctionField.objects.create(definition=definition, **field)
        return definition


class FunctionNodeSerializer(BaseNodeSerializer):
    slots = SlotSerializer(many=True, read_only=True)

    class Meta(BaseNodeSerializer.Meta):
        model = FunctionNode
        fields = "__all__"

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
