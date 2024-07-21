from django.contrib import admin

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from apps.flow_new.models import (
    Tag,
    BaseModelWithTag,
    FileArchive,
    Dependency,
    Flow,
    Slot,
    Connection,
    FunctionDefinition,
    BaseNode,
    FunctionField,
    FunctionNode,
    DataNode,
    FlowNode,
    InputNode,
    OutputNode,
    ConditionalNode,
    ForEachNode,
    ScopeBlock,
)

from apps.trigger.models import WebHookTrigger, PeriodicTrigger


@admin.register(BaseModelWithTag)
class BaseModelWithTagAdmin(PolymorphicParentModelAdmin):
    base_model = BaseModelWithTag
    child_models = (
        FileArchive,
        Dependency,
        Flow,
        FunctionDefinition,
        PeriodicTrigger,
        WebHookTrigger,
    )


@admin.register(BaseNode)
class BaseNodeAdmin(PolymorphicParentModelAdmin):
    base_model = BaseNode
    child_models = (
        FunctionNode,
        DataNode,
        FlowNode,
        InputNode,
        OutputNode,
        ConditionalNode,
        ForEachNode,
    )


@admin.register(FunctionNode)
class FunctionNodeAdmin(PolymorphicChildModelAdmin):
    base_model = FunctionNode


@admin.register(DataNode)
class DataNodeAdmin(PolymorphicChildModelAdmin):
    base_model = DataNode


@admin.register(FlowNode)
class FlowNodeAdmin(PolymorphicChildModelAdmin):
    base_model = FlowNode


@admin.register(InputNode)
class InputNodeAdmin(PolymorphicChildModelAdmin):
    base_model = InputNode


@admin.register(OutputNode)
class OutputNodeAdmin(PolymorphicChildModelAdmin):
    base_model = OutputNode


@admin.register(ConditionalNode)
class ConditionalAdmin(PolymorphicChildModelAdmin):
    base_model = ConditionalNode


@admin.register(ForEachNode)
class ForEachNodeAdmin(PolymorphicChildModelAdmin):
    base_model = ForEachNode


@admin.register(FileArchive)
class FileArchiveAdmin(PolymorphicChildModelAdmin):
    base_model = FileArchive


@admin.register(Dependency)
class DependencyAdmin(PolymorphicChildModelAdmin):
    base_model = Dependency


@admin.register(Flow)
class FlowAdmin(PolymorphicChildModelAdmin):
    base_model = Flow


@admin.register(FunctionDefinition)
class FunctionDefinitionAdmin(PolymorphicChildModelAdmin):
    base_model = FunctionDefinition


admin.site.register(Tag)
admin.site.register(Slot)
admin.site.register(Connection)
admin.site.register(FunctionField)
admin.site.register(ScopeBlock)
