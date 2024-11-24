from apps.flow.enums import ITEM_TYPE

from apps.flow.serializers import (
    FileArchiveSerializer,
    FlowSerializer,
    FunctionDefinitionSerializer,
    DependencySerializer,
)
from apps.trigger.serializers import PeriodicTriggerSerializer, WebHookTriggerSerializer
from apps.flow.models import FileArchive, Flow, FunctionDefinition, Dependency
from apps.trigger.models import PeriodicTrigger, WebHookTrigger


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
    ITEM_TYPE.WEBHOOK.value: {
        "serializer": WebHookTriggerSerializer,
        "model": WebHookTrigger,
    },
    ITEM_TYPE.PERIODIC.value: {
        "serializer": PeriodicTriggerSerializer,
        "model": PeriodicTrigger,
    },
}
