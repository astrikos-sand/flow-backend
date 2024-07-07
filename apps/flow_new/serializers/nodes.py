from rest_framework import serializers

from rest_polymorphic.serializers import PolymorphicSerializer

from apps.flow_new.models import (
    BaseNode,
    DataNode,
    ConditionalNode,
    Slot,
    Connection,
)

# TODO: Complete the following serializers


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = "__all__"


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = "__all__"


class BaseNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseNode
        fields = "__all__"


class DataNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataNode
        fields = "__all__"


class ConditionalNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionalNode
        fields = "__all__"


class BaseNodePolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = "cls_type"

    model_serializer_mapping = {
        BaseNode: BaseNodeSerializer,
        DataNode: DataNodeSerializer,
        ConditionalNode: ConditionalNodeSerializer,
    }
