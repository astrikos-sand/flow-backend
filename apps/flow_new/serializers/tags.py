from rest_framework import serializers

from rest_polymorphic.serializers import PolymorphicSerializer

from apps.flow_new.models import (
    Tag,
    FileArchive,
    BaseModelWithTag,
)

# TODO: Complete the following serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class FileArchiveSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)

    class Meta:
        model = FileArchive
        fields = "__all__"


class BaseModelWithTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModelWithTag
        fields = "__all__"


class BaseModelWithTagPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = "cls_type"

    model_serializer_mapping = {
        BaseModelWithTag: BaseModelWithTagSerializer,
    }
