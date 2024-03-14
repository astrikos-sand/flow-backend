from django.contrib import admin
from apps.flow.models import (
    FlowFile,
    DataNodeClass,
    DynamicNodeClass,
    Node,
    Parameter,
    Connections,
)

# Register your models here.
admin.site.register(FlowFile)
admin.site.register(DataNodeClass)
admin.site.register(DynamicNodeClass)
admin.site.register(Node)
admin.site.register(Parameter)
admin.site.register(Connections)
