from django.contrib import admin

from polymorphic.admin import PolymorphicChildModelAdmin

from apps.trigger.models import (
    WebHookTrigger,
    PeriodicTrigger,
)


@admin.register(WebHookTrigger)
class WebHookTriggerAdmin(PolymorphicChildModelAdmin):
    base_model = WebHookTrigger


@admin.register(PeriodicTrigger)
class PeriodicTriggerAdmin(PolymorphicChildModelAdmin):
    base_model = PeriodicTrigger
