from apps.flow_new.enums import ITEM_TYPE
from apps.flow_new.serializers import (
    FileArchiveSerializer,
    FlowSerializer,
    DependencySerializer,
    FunctionDefinitionSerializer,
)
from apps.flow_new.models import FileArchive, Flow, Dependency, FunctionDefinition
from apps.trigger.models import PeriodicTrigger, WebHookTrigger
from apps.trigger.serializers import PeriodicTriggerSerializer, WebHookTriggerSerializer

ITEM_MAPS = {
    ITEM_TYPE.ARCHIVES.value: {
        "serializer": FileArchiveSerializer,
        "model": FileArchive,
    },
    ITEM_TYPE.FLOW.value: {
        "serializer": FlowSerializer,
        "model": Flow,
    },
    ITEM_TYPE.DEPENDENCY.value: {
        "serializer": DependencySerializer,
        "model": Dependency,
    },
    ITEM_TYPE.FUNCTION_DEFINITION.value: {
        "serializer": FunctionDefinitionSerializer,
        "model": FunctionDefinition,
    },
    ITEM_TYPE.PERIODIC_TRIGGER.value: {
        "serializer": PeriodicTriggerSerializer,
        "model": PeriodicTrigger,
    },
    ITEM_TYPE.WEBHOOK_TRIGGER.value: {
        "serializer": WebHookTriggerSerializer,
        "model": WebHookTrigger,
    },
}
