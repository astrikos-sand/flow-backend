from rest_framework import serializers

from apps.flow.models import (
    FunctionField,
    FunctionDefinition,
    FunctionNode,
    Slot,
    Prefix,
)
from apps.flow.serializers.nodes import BaseNodeSerializer
from apps.flow.serializers.prefix import PrefixSerializer
from apps.flow.enums import ITEM_TYPE


class FunctionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionField
        exclude = (
            "definition",
            "created_at",
            "updated_at",
        )


class FunctionDefinitionSerializer(serializers.ModelSerializer):
    fields = FunctionFieldSerializer(many=True, write_only=True, required=False)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if instance.prefix is not None:
    #         data["prefix"] = PrefixSerializer(instance.prefix).data
    #     return data

    class Meta:
        model = FunctionDefinition
        exclude = (
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        prefix: Prefix | None = validated_data.get("prefix", None)
        if prefix is None:
            root = Prefix.objects.get(name=ITEM_TYPE.FUNCTION.value)
            misc_prefix = Prefix.objects.get(name="miscellaneous", parent=root)
            validated_data["prefix"] = misc_prefix
        else:
            if not prefix.full_name.startswith(ITEM_TYPE.FUNCTION.value):
                raise serializers.ValidationError("Prefix must start with 'flows'")

        fields = validated_data.pop("fields", [])
        definition = FunctionDefinition.objects.create(**validated_data)
        for field in fields:
            FunctionField.objects.create(definition=definition, **field)
        return definition

    def update(self, instance, validated_data):
        if "fields" in validated_data:
            validated_data.pop("fields")

        return super().update(instance, validated_data)


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
