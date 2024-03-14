from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from apps.resource.models import ResourceGroup, ResourcePermission


class ResourceAdmin(TreeAdmin):
    form = movenodeform_factory(ResourceGroup)
    readonly_fields = ("id",)


admin.site.register(ResourceGroup, ResourceAdmin)
admin.site.register(ResourcePermission)
