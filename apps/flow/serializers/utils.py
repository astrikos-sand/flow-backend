from apps.flow.models import DAGMetaData

from rest_framework import serializers


class DAGMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DAGMetaData
        exclude = (
            "created_at",
            "updated_at",
        )
