from apps.flow.enums import ITEM_TYPE

from apps.flow.serializers import (
    FileArchiveSerializer,
    FlowSerializer,
    FunctionDefinitionSerializer,
    DependencySerializer,
)
from apps.flow.models import FileArchive, Flow, FunctionDefinition, Dependency


ITEM_MAPS = {
    ITEM_TYPE.ARCHIVES.value: {
        "serializer": FileArchiveSerializer,
        "model": FileArchive,
    },
    ITEM_TYPE.FLOW.value: {
        "serializer": FlowSerializer,
        "model": Flow,
    },
    ITEM_TYPE.FUNCTION.value: {
        "serializer": FunctionDefinitionSerializer,
        "model": FunctionDefinition,
    },
    ITEM_TYPE.DEPENDENCY.value: {
        "serializer": DependencySerializer,
        "model": Dependency,
    },
}
