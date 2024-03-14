from django.contrib import admin

from apps.iam.models import (
    Role,
    IAMUser,
)


admin.site.register(IAMUser)
admin.site.register(Role)
