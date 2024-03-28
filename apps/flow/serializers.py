from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from apps.flow.models import (
    BaseNode,
    DataNode,
    GenericNode,
    GenericNodeClass,
    TriggerNodeClass,
    BaseNodeClass,
    FlowFile,
    Slot,
    Connection,
)


class ConnectionSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = ("id", "source", "target", "source_slot", "target_slot")

    def validate(self, data: dict):
        source: BaseNode = data.get("source")
        target: BaseNode = data.get("target")

        source_slot = data.get("source_slot")
        target_slot = data.get("target_slot")

        if source.id == target.id:
            raise serializers.ValidationError("source and target can't be same")

        if source_slot not in source.get_real_instance().output_slots.values_list(
            "name", flat=True
        ):
            raise serializers.ValidationError("source slot not found in source node")

        if target_slot not in target.get_real_instance().input_slots.values_list(
            "name", flat=True
        ):
            raise serializers.ValidationError("target slot not found in target node")

        return super().validate(data)


class GenericNodeSerializer(serializers.ModelSerializer):
    node_class_type = serializers.ReadOnlyField(read_only=True)
    node_class_name = serializers.ReadOnlyField(read_only=True)
    input_slots = serializers.ReadOnlyField(read_only=True)
    output_slots = serializers.ReadOnlyField(read_only=True)
    special_slots = serializers.ReadOnlyField(read_only=True)
    code = serializers.FileField(read_only=True)
    source_connections = ConnectionSerialzer(many=True)
    target_connections = ConnectionSerialzer(many=True)

    class Meta:
        model = GenericNode
        fields = (
            "id",
            "node_class",
            "input_slots",
            "output_slots",
            "special_slots",
            "node_class_type",
            "node_class_name",
            "source_connections",
            "target_connections",
            "code",
        )


class DataNodeSerializer(serializers.ModelSerializer):
    input_slots = serializers.ReadOnlyField(read_only=True)
    output_slots = serializers.ReadOnlyField(read_only=True)
    special_slots = serializers.ReadOnlyField(read_only=True)
    source_connections = ConnectionSerialzer(many=True)
    target_connections = ConnectionSerialzer(many=True)

    class Meta:
        model = DataNode
        fields = (
            "id",
            "input_slots",
            "output_slots",
            "special_slots",
            "value",
            "type",
            "source_connections",
            "target_connections",
        )


class BaseNodeSerializer(PolymorphicSerializer):
    resource_type_field_name = "node_type"
    input_slots = serializers.ReadOnlyField(read_only=True)
    output_slots = serializers.ReadOnlyField(read_only=True)
    source_connections = ConnectionSerialzer(many=True)
    target_connections = ConnectionSerialzer(many=True)

    model_serializer_mapping = {
        DataNode: DataNodeSerializer,
        GenericNode: GenericNodeSerializer,
    }

    class Meta:
        model = BaseNode
        fields = "__all__"


class SlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slot
        fields = ("id", "name", "attachment_type")


class GenericNodeClassSerializer(serializers.ModelSerializer):

    slots = SlotSerializer(many=True)

    class Meta:
        model = GenericNodeClass
        fields = ("id", "name", "description", "code", "slots")


class TriggerNodeClassSerializer(serializers.ModelSerializer):

    slots = SlotSerializer(many=True)

    class Meta:
        model = TriggerNodeClass
        fields = ("id", "name", "description", "code", "slots")


class BaseNodeClassSerializer(PolymorphicSerializer):
    resource_type_field_name = "node_class_type"

    model_serializer_mapping = {
        GenericNodeClass: GenericNodeClassSerializer,
        TriggerNodeClass: TriggerNodeClassSerializer,
    }

    class Meta:
        model = BaseNodeClass
        fields = "__all__"


class FlowFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowFile
        fields = ("id", "name", "nodes", "description")
