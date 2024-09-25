from rest_polymorphic.serializers import PolymorphicSerializer

from apps.flow.serializers.nodes import (
    BaseNodeSerializer,
    DataNodeSerializer,
)
from apps.flow.serializers.function import FunctionNodeSerializer
from apps.flow.serializers.flow import (
    FlowNodeSerializer,
    InputNodeSerializer,
    OutputNodeSerializer,
)
from apps.flow.serializers.for_each import (
    ForEachNodeSerializer,
    BlockNodeSerializer,
)
from apps.flow.serializers.conditional import ConditionalNodeSerializer

from apps.flow.models import (
    BaseNode,
    DataNode,
    ConditionalNode,
    FunctionNode,
    FlowNode,
    InputNode,
    OutputNode,
    ForEachNode,
    BlockNode,
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
        ForEachNode: ForEachNodeSerializer,
        BlockNode: BlockNodeSerializer,
    }
