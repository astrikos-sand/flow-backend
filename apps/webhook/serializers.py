from rest_framework.serializers import ModelSerializer

from apps.webhook.models import WebHookEvent


class WebHookEventSerializer(ModelSerializer):
    class Meta:
        model = WebHookEvent
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
