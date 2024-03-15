from django.contrib import admin

from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
)

from apps.flow.models import (
    FlowFile,
    DynamicNodeClass,
    BaseNode,
    Slot,
    DynamicNode,
    DataNode,
    Connection,
)

# Register your models here.
admin.site.register(FlowFile)
admin.site.register(DynamicNodeClass)
admin.site.register(Slot)
admin.site.register(Connection)


class BaseNodeChildAdmin(PolymorphicChildModelAdmin):
    base_model = BaseNode


@admin.register(DynamicNode)
class DynamicNodeAdmin(PolymorphicChildModelAdmin):
    base_model = DynamicNode


@admin.register(DataNode)
class DataNodeAdmin(PolymorphicChildModelAdmin):
    base_model = DataNode


@admin.register(BaseNode)
class BaseNodeAdmin(PolymorphicParentModelAdmin):
    base_model = BaseNode
    child_models = (DynamicNode, DataNode)
    list_filter = (PolymorphicChildModelFilter,)
    child_model_admin = BaseNodeChildAdmin
