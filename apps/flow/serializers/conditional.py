from rest_framework import serializers

from apps.flow.enums import ATTACHMENT_TYPE
from apps.flow.models import ConditionalNode, ConditionalNodeCase, Slot
from apps.flow.serializers.nodes import BaseNodeSerializer, SlotSerializer
from apps.flow.serializers.flow import ScopeSerializer

from apps.flow.utils import typecast_value


class ConditionalNodeCaseSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    block = ScopeSerializer(read_only=True)

    class Meta:
        model = ConditionalNodeCase
        exclude = (
            "created_at",
            "updated_at",
            "node",
        )


class ConditionalNodeSerializer(BaseNodeSerializer):
    slots = SlotSerializer(many=True, write_only=True)
    cases = ConditionalNodeCaseSerializer(many=True)

    class Meta(BaseNodeSerializer.Meta):
        model = ConditionalNode

    def create(self, validated_data):
        slots = validated_data.pop("slots")
        cases = validated_data.pop("cases")
        value_type = validated_data.get("value_type")

        input_slots = [
            {
                "name": "_condition",
                "attachment_type": ATTACHMENT_TYPE.INPUT.value,
                "value_type": value_type,
            }
        ]

        input_slots = input_slots + [
            slot
            for slot in slots
            if slot["attachment_type"] == ATTACHMENT_TYPE.INPUT.value
        ]

        case = [
            {
                "name": "_case",
                "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
                "value_type": value_type,
            }
        ]

        output_slots = case + [
            {
                **slot,
                "attachment_type": ATTACHMENT_TYPE.OUTPUT.value,
            }
            for slot in input_slots[1:]
        ]

        slots = input_slots + output_slots

        if len(cases) < 1:
            raise serializers.ValidationError("At least one case is required")

        for case in cases:
            value = case.get("value", None)
            if value is None:
                raise serializers.ValidationError("Value for case is missing")
            try:
                typecast_value(value, value_type)
            except Exception as e:
                raise serializers.ValidationError(
                    f"Unable to typecast {value} to {value_type}"
                )

        default_case = [
            {
                "name": "_default",
            }
        ]

        cases = cases + default_case

        conditional_node = ConditionalNode.objects.create(**validated_data)

        for slot in slots:
            data = {
                "name": slot["name"],
                "attachment_type": slot["attachment_type"],
            }

            slot_value_type = slot.get("value_type", None)
            if slot_value_type:
                data["value_type"] = slot_value_type

            Slot.objects.create(node=conditional_node, **data)

        scope_input_slots = [
            {
                **slot,
                "attachment_type": ATTACHMENT_TYPE.INPUT.value,
            }
            for slot in output_slots
        ]
        for case in cases:
            scope_serializer = ScopeSerializer(
                data={
                    "name": case.pop("name"),
                    "slots": scope_input_slots,
                    "scope": validated_data["flow"].id,
                }
            )
            scope_serializer.is_valid(raise_exception=True)
            print(2)
            scope_serializer.save()
            print(3)
            ConditionalNodeCase.objects.create(
                value=case.get("value", None),
                node=conditional_node,
                block=scope_serializer.instance,
            )

        return conditional_node
