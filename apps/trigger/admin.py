from django.contrib import admin
from apps.trigger.models import WebHookTrigger, PeriodicTrigger

admin.site.register(WebHookTrigger)
admin.site.register(PeriodicTrigger)

# Register your models here.
