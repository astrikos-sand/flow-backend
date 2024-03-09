from django.contrib import admin

from apps.iam.models import (
    Policy,
    Role,
    IAMUser,
    ResourcePermission,
    PolicyResourcePermissionRelation,
)


class PolicyResourcePermissionInline(admin.TabularInline):
    model = PolicyResourcePermissionRelation
    extra = 1


class PolicyAdmin(admin.ModelAdmin):
    inlines = (PolicyResourcePermissionInline,)


admin.site.register(IAMUser)
admin.site.register(ResourcePermission)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(Role)
