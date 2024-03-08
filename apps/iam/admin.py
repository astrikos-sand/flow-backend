from django.contrib import admin

from apps.iam.models import Policy, Role, IAMUser, ResourcePermission

admin.site.register(IAMUser)
admin.site.register(ResourcePermission)
admin.site.register(Policy)
admin.site.register(Role)
