from django.contrib import admin

from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
)

from apps.flow.models import (
    FlowFile,
    BaseNodeClass,
    GenericNodeClass,
    TriggerNodeClass,
    BaseNode,
    Slot,
    GenericNode,
    DataNode,
    Connection,
    NodeResult,
)

# Register your models here.
admin.site.register(FlowFile)
admin.site.register(Slot)
admin.site.register(Connection)


# BaseNodeClass Polymorphic Admin
class BaseNodeClassChildAdmin(PolymorphicChildModelAdmin):
    base_model = BaseNodeClass


@admin.register(GenericNodeClass)
class GenericNodeClassAdmin(BaseNodeClassChildAdmin):
    base_model = GenericNodeClass


@admin.register(TriggerNodeClass)
class TriggerNodeClassAdmin(BaseNodeClassChildAdmin):
    base_model = TriggerNodeClass


@admin.register(BaseNodeClass)
class BaseNodeClassAdmin(PolymorphicParentModelAdmin):
    base_model = BaseNodeClass
    child_models = (GenericNodeClass, TriggerNodeClass)
    list_filter = (PolymorphicChildModelFilter,)
    child_model_admin = BaseNodeClassChildAdmin


# BaseNode Polymorphic Admin
class BaseNodeChildAdmin(PolymorphicChildModelAdmin):
    base_model = BaseNode


@admin.register(GenericNode)
class GenericNodeAdmin(PolymorphicChildModelAdmin):
    base_model = GenericNode


@admin.register(DataNode)
class DataNodeAdmin(PolymorphicChildModelAdmin):
    base_model = DataNode


@admin.register(BaseNode)
class BaseNodeAdmin(PolymorphicParentModelAdmin):
    base_model = BaseNode
    child_models = (GenericNode, DataNode)
    list_filter = (PolymorphicChildModelFilter,)
    child_model_admin = BaseNodeChildAdmin


admin.site.register(NodeResult)
