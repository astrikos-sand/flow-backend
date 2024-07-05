from rest_framework import serializers

from apps.flow_new.models import Tag, FileArchive


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class FileArchiveSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="url", read_only=True)

    class Meta:
        model = FileArchive
        fields = "__all__"
