from rest_framework import serializers

from apps.flow_new.models import (
    BaseNode,
    DataNode,
    ConditionalNode,
    Slot,
    Connection,
    Flow,
    Dependency,
    ConditionalNodeValue,
)
from apps.flow_new.enums import ATTACHMENT_TYPE


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        exclude = (
            "created_at",
            "updated_at",
        )


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        exclude = (
            "created_at",
            "updated_at",
        )


class ConnectionSerializer(serializers.ModelSerializer):
    source = serializers.UUIDField(source="from_slot.node.id", read_only=True)
    target = serializers.UUIDField(source="to_slot.node.id", read_only=True)

    class Meta:
        model = Connection
        exclude = (
            "created_at",
            "updated_at",
        )


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        exclude = (
            "node",
            "created_at",
            "updated_at",
        )


class BaseNodeSerializer(serializers.ModelSerializer):
    input_slots = SlotSerializer(many=True, read_only=True)
    output_slots = SlotSerializer(many=True, read_only=True)
    connections_in = ConnectionSerializer(many=True, read_only=True)
    connections_out = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = BaseNode
        exclude = (
            "created_at",
            "updated_at",
        )


class DataNodeSerializer(BaseNodeSerializer):
    value_type = serializers.CharField(write_only=True)

    class Meta(BaseNodeSerializer.Meta):
        model = DataNode

    def create(self, validated_data):
        value_type = validated_data.pop("value_type")

        data_node = DataNode.objects.create(**validated_data)
        data = {
            "name": data_node.name,
            "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
            "value_type": value_type,
        }

        Slot.objects.create(node=data_node, **data)
        return data_node


class ConditionalNodeSerializer(BaseNodeSerializer):
    slots = SlotSerializer(many=True, write_only=True)
    values = serializers.DictField(write_only=True)

    def get_values(self, obj):
        output_slots = obj.slots.filter(attachment_type=ATTACHMENT_TYPE.OUTPUT.value)
        values = {}
        for slot in output_slots:
            value = slot.conditional_node_value.value
            values[slot.name] = value

        return values

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["values"] = self.get_values(instance)
        return representation

    class Meta(BaseNodeSerializer.Meta):
        model = ConditionalNode

    def create(self, validated_data):
        slots = validated_data.pop("slots")
        values = validated_data.pop("values")

        input_slots = [
            slot
            for slot in slots
            if slot["attachment_type"] == ATTACHMENT_TYPE.INPUT.value
        ]
        output_slots = [
            slot
            for slot in slots
            if slot["attachment_type"] == ATTACHMENT_TYPE.OUTPUT.value
        ]

        if len(input_slots) != 1:
            raise serializers.ValidationError(
                "ConditionalNode should have exactly one input slot"
            )

        if len(output_slots) < 2:
            raise serializers.ValidationError(
                "ConditionalNode should have at least two output slots"
            )

        for output_slot in output_slots:
            value = values.get(output_slot["name"], None)
            if value is None:
                raise serializers.ValidationError(
                    f"Value for slot {output_slot['name']} is missing"
                )

        conditional_node = ConditionalNode.objects.create(**validated_data)

        for slot in slots:
            data = {
                "name": slot["name"],
                "attachment_type": slot["attachment_type"],
            }

            value_type = slot.get("value_type", None)
            if value_type:
                data["value_type"] = value_type

            instance = Slot.objects.create(node=conditional_node, **data)

            value = values.get(slot["name"], None)
            if value is not None:
                ConditionalNodeValue.objects.create(slot=instance, value=value)

        return conditional_node
