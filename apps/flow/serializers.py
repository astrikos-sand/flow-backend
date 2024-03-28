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


class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = ("id", "source", "target", "source_slot", "target_slot")


class GenericNodeSerializer(serializers.ModelSerializer):
    node_class_type = serializers.ReadOnlyField(read_only=True)
    input_slots = serializers.ReadOnlyField(read_only=True)
    output_slots = serializers.ReadOnlyField(read_only=True)
    special_slots = serializers.ReadOnlyField(read_only=True)
    code = serializers.FileField(read_only=True)
    source_connections = ConnectionSerializer(many=True)
    target_connections = ConnectionSerializer(many=True)

    class Meta:
        model = GenericNode
        fields = (
            "id",
            "node_class",
            "input_slots",
            "output_slots",
            "special_slots",
            "node_class_type",
            "source_connections",
            "target_connections",
            "code",
            "flow_file",
            "position"
        )

    def create(self, validated_data):
        source_connections_data = validated_data.pop('source_connections', [])
        target_connections_data = validated_data.pop('target_connections', [])
        
        generic_node = GenericNode.objects.create(**validated_data)

        for connection_data in source_connections_data:
            Connection.objects.create(source=generic_node, **connection_data)
        
        for connection_data in target_connections_data:
            Connection.objects.create(target=generic_node, **connection_data)

        return generic_node

class DataNodeSerializer(serializers.ModelSerializer):
    input_slots = serializers.ReadOnlyField(read_only=True)
    output_slots = serializers.ReadOnlyField(read_only=True)
    special_slots = serializers.ReadOnlyField(read_only=True)
    source_connections = ConnectionSerializer(many=True)

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
            "flow_file",
            "position"
        )

    def create(self, validated_data):
        source_connections_data = validated_data.pop('source_connections', [])
        target_connections_data = validated_data.pop('target_connections', [])
        
        data_node = DataNode.objects.create(**validated_data)

        for connection_data in source_connections_data:
            Connection.objects.create(source=data_node, **connection_data)
        
        for connection_data in target_connections_data:
            Connection.objects.create(target=data_node, **connection_data)

        return data_node

class BaseNodeSerializer(PolymorphicSerializer):
    resource_type_field_name = "node_type"
    input_slots = serializers.ReadOnlyField(read_only=True)
    output_slots = serializers.ReadOnlyField(read_only=True)
    source_connections = ConnectionSerializer(many=True)
    flow_file_id = serializers.UUIDField()

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

    def create(self, validated_data):
        print(validated_data)
        slots_data = validated_data.pop('slots')
        generic_node_class = GenericNodeClass.objects.create(**validated_data)
        for slot_data in slots_data:
            Slot.objects.create(node_class=generic_node_class, **slot_data)
        return generic_node_class

class TriggerNodeClassSerializer(serializers.ModelSerializer):

    slots = SlotSerializer(many=True)

    class Meta:
        model = TriggerNodeClass
        fields = ("id", "name", "description", "slots")


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
    nodes = BaseNodeSerializer(many=True)

    class Meta:
        model = FlowFile
        fields = ("id", "name", "nodes", "description")
