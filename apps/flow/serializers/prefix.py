from rest_framework import serializers

from apps.flow.models import FileArchive, Prefix


class PrefixSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Prefix
        exclude = (
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "name": {"write_only": True},
            "parent": {"write_only": True},
        }

    def validate_parent(self, value):
        if not value:
            raise serializers.ValidationError("Parent cannot be empty")

        return value


class FileArchiveSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)

    class Meta:
        model = FileArchive
        exclude = (
            "created_at",
            "updated_at",
        )
