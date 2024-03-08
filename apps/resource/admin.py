from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from apps.resource.models import ResourceGroup


class ResourceAdmin(TreeAdmin):
    form = movenodeform_factory(ResourceGroup)


admin.site.register(ResourceGroup, ResourceAdmin)
