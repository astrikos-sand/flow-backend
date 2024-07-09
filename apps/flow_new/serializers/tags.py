from rest_framework import serializers

from rest_polymorphic.serializers import PolymorphicSerializer

from apps.flow_new.models import (
    Tag,
    FileArchive,
    BaseModelWithTag,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = (
            "created_at",
            "updated_at",
        )


class FileArchiveSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)

    class Meta:
        model = FileArchive
        exclude = (
            "created_at",
            "updated_at",
        )


class BaseModelWithTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModelWithTag
        exclude = (
            "created_at",
            "updated_at",
        )


class BaseModelWithTagPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = "item_type"

    model_serializer_mapping = {
        BaseModelWithTag: BaseModelWithTagSerializer,
        FileArchive: FileArchiveSerializer,
    }
