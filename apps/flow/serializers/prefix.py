from rest_framework import serializers

from apps.flow.models import FileArchive, Prefix, Flow, Dependency, FlowExecution
from apps.flow.enums import ITEM_TYPE


class PrefixSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Prefix
        exclude = (
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "parent": {"write_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        parent = attrs.get("parent", None)

        if parent is None:
            raise serializers.ValidationError("Parent cannot be empty")

        return attrs


class FlowSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if instance.prefix is not None:
    #         data["prefix"] = PrefixSerializer(instance.prefix).data
    #     return data

    def validate(self, attrs):
        attrs = super().validate(attrs)

        prefix: Prefix | None = attrs.get("prefix", None)
        if prefix is None:
            root = Prefix.objects.get(name=ITEM_TYPE.FLOW.value)
            misc_prefix = Prefix.objects.get(name="miscellaneous", parent=root)
            attrs["prefix"] = misc_prefix
        else:
            if not prefix.full_name.startswith(ITEM_TYPE.FLOW.value):
                raise serializers.ValidationError("Prefix must start with 'flows'")

        return attrs

    class Meta:
        model = Flow
        exclude = (
            "created_at",
            "updated_at",
        )


class FileArchiveSerializer(serializers.ModelSerializer):
    url = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        prefix: Prefix | None = attrs.get("prefix", None)
        if prefix is None:
            root = Prefix.objects.get(name=ITEM_TYPE.ARCHIVES.value)
            misc_prefix = Prefix.objects.get(name="miscellaneous", parent=root)
            attrs["prefix"] = misc_prefix
        else:
            if not prefix.full_name.startswith(ITEM_TYPE.ARCHIVES.value):
                raise serializers.ValidationError("Prefix must start with 'flows'")

        return attrs

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if instance.prefix is not None:
    #         data["prefix"] = PrefixSerializer(instance.prefix).data
    #     return data

    class Meta:
        model = FileArchive
        exclude = (
            "created_at",
            "updated_at",
        )


class DependencySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)

        prefix: Prefix | None = attrs.get("prefix", None)
        if prefix is None:
            root = Prefix.objects.get(name=ITEM_TYPE.DEPENDENCY.value)
            misc_prefix = Prefix.objects.get(name="miscellaneous", parent=root)
            attrs["prefix"] = misc_prefix
        else:
            if not prefix.full_name.startswith(ITEM_TYPE.DEPENDENCY.value):
                raise serializers.ValidationError("Prefix must start with 'flows'")

        return attrs

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if instance.prefix is not None:
    #         data["prefix"] = PrefixSerializer(instance.prefix).data
    #     return data

    class Meta:
        model = Dependency
        exclude = (
            "created_at",
            "updated_at",
        )


class FlowExecutionSerializer(serializers.ModelSerializer):
    timestamp = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.html_logs is not None:
            data.update(
                {
                    "html_logs": FileArchive.objects.get(id=instance.html_logs.id).url,
                }
            )

        if instance.json_logs is not None:
            data.update(
                {
                    "json_logs": FileArchive.objects.get(id=instance.json_logs.id).url,
                }
            )
        
        if instance.container_logs is not None:
            data.update(
                {
                    "container_logs": FileArchive.objects.get(
                        id=instance.container_logs.id
                    ).url,
                }
            )

        return data

    class Meta:
        model = FlowExecution
        exclude = (
            "created_at",
            "updated_at",
        )
