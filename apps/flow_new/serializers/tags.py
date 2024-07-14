from rest_framework import serializers

from rest_polymorphic.serializers import PolymorphicSerializer

from apps.flow_new.models import (
    Tag,
    FileArchive,
    BaseModelWithTag,
)


class TagSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        exclude = (
            "created_at",
            "updated_at",
        )

    def get_children(self, obj):
        return TagSerializer(obj.children, many=True).data

    def get_full_name(self, obj):
        return obj.full_name


class FileArchiveSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = FileArchive
        exclude = (
            "created_at",
            "updated_at",
        )
        fields = ["id", "name", "file", "tags"]


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
