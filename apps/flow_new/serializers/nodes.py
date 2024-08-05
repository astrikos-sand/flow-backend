from rest_framework import serializers

from apps.flow_new.models import (
    BaseNode,
    DataNode,
    ConditionalNode,
    Slot,
    Connection,
    Flow,
    Dependency,
)
from apps.flow_new.enums import ATTACHMENT_TYPE
from apps.flow_new.utils import typecast_value
from apps.flow_new.serializers.tags import TagSerializer


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        exclude = (
            "created_at",
            "updated_at",
        )


class FlowSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    full_name = serializers.CharField(read_only=True)
    environment = DependencySerializer(source="lib", read_only=True)

    class Meta:
        model = Flow
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
    class Meta(BaseNodeSerializer.Meta):
        model = DataNode

    def create(self, validated_data):
        try:
            value = validated_data["value"]
            value_type = validated_data["value_type"]
            typecast_value(value, value_type)
        except Exception as e:
            raise serializers.ValidationError(
                f"Unable to typecast {value} to {value_type}"
            )

        data_node = DataNode.objects.create(**validated_data)
        data = {
            "name": data_node.name,
            "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
            "value_type": data_node.value_type,
        }

        Slot.objects.create(node=data_node, **data)
        return data_node
