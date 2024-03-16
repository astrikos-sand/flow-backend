from django.contrib import admin

from apps.webhook.models import WebHookEvent

# Register your models here.
admin.site.register(WebHookEvent)
