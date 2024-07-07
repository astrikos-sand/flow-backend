from rest_framework import serializers

from apps.flow_new.models import FunctionField, FunctionDefinition, FunctionNode


class FunctionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionField
        fields = "__all__"


class FunctionDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionDefinition
        fields = "__all__"


# TODO: Add FunctionNodeSerializer
