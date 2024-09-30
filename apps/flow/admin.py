from django.contrib import admin

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from apps.flow.models import (
    FileArchive,
    Dependency,
    Flow,
    FunctionDefinition,
    Prefix,
    Slot,
    Connection,
    BaseNode,
    FunctionField,
    FunctionNode,
    DataNode,
    FlowNode,
    InputNode,
    OutputNode,
    ConditionalNode,
    ConditionalNodeCase,
    ForEachNode,
    ScopeBlock,
    BlockNode,
    FlowExecution,
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
        BlockNode,
    )


admin.site.register(Prefix)
admin.site.register(Flow)
admin.site.register(FunctionDefinition)
admin.site.register(FileArchive)
admin.site.register(Dependency)
admin.site.register(Slot)
admin.site.register(Connection)
admin.site.register(FunctionField)
admin.site.register(ScopeBlock)
admin.site.register(ConditionalNodeCase)
admin.site.register(FlowExecution)


@admin.register(BlockNode)
class BlockNodeAdmin(PolymorphicChildModelAdmin):
    base_model = BlockNode


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
