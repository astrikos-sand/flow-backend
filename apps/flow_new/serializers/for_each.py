from rest_framework import serializers

from apps.flow_new.enums import ATTACHMENT_TYPE, VALUE_TYPE
from apps.flow_new.models import ForEachNode, Slot
from apps.flow_new.serializers.nodes import (
    BaseNodeSerializer,
    SlotSerializer,
)

from apps.flow_new.serializers.flow import ScopeSerializer


class ForEachNodeSerializer(BaseNodeSerializer):
    slots = SlotSerializer(many=True, write_only=True)
    name = serializers.CharField()
    block = ScopeSerializer(read_only=True)

    class Meta(BaseNodeSerializer.Meta):
        model = ForEachNode

    def create(self, validated_data):
        slots = validated_data.pop("slots")

        input_slots = [
            {
                "name": "_list",
                "attachment_type": ATTACHMENT_TYPE.INPUT.value,
                "value_type": VALUE_TYPE.LIST.value,
            }
        ]

        input_slots = input_slots + [
            slot
            for slot in slots
            if slot["attachment_type"] == ATTACHMENT_TYPE.INPUT.value
        ]

        output_slots = [
            {
                "name": slot["name"],
                "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
            }
            for slot in input_slots[1:]
        ]

        slots = input_slots + output_slots

        scope_input_slots = [
            {
                "name": "_element",
                "attachment_type": ATTACHMENT_TYPE.INPUT.value,
            }
        ] + input_slots[1:]

        scope_serializer = ScopeSerializer(
            data={
                "name": validated_data.pop("name"),
                "slots": scope_input_slots,
                "scope": validated_data["flow"],
            }
        )

        scope_serializer.is_valid(raise_exception=True)
        scope_serializer.save()

        validated_data["block"] = scope_serializer.instance

        for_each_node = ForEachNode.objects.create(**validated_data)

        for slot in slots:
            data = {
                "name": slot["name"],
                "attachment_type": slot["attachment_type"],
            }
            Slot.objects.create(node=for_each_node, **data)

        return for_each_node
