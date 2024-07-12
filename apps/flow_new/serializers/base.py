from rest_polymorphic.serializers import PolymorphicSerializer

from apps.flow_new.serializers.nodes import (
    BaseNodeSerializer,
    DataNodeSerializer,
    ConditionalNodeSerializer,
)
from apps.flow_new.serializers.function import FunctionNodeSerializer
from apps.flow_new.serializers.flow import (
    FlowNodeSerializer,
    InputNodeSerializer,
    OutputNodeSerializer,
)

from apps.flow_new.models import (
    BaseNode,
    DataNode,
    ConditionalNode,
    FunctionNode,
    FlowNode,
    InputNode,
    OutputNode,
)


class BaseNodePolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = "node_type"

    model_serializer_mapping = {
        BaseNode: BaseNodeSerializer,
        DataNode: DataNodeSerializer,
        ConditionalNode: ConditionalNodeSerializer,
        FunctionNode: FunctionNodeSerializer,
        FlowNode: FlowNodeSerializer,
        InputNode: InputNodeSerializer,
        OutputNode: OutputNodeSerializer,
    }