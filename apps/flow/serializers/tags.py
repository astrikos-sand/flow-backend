from rest_framework import serializers

from apps.flow.models import (
    FileArchive,
)


class FileArchiveSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)

    class Meta:
        model = FileArchive
        exclude = (
            "created_at",
            "updated_at",
        )
