from rest_framework import serializers

from apps.flow_new.enums import ATTACHMENT_TYPE

from apps.flow_new.models import FlowNode, InputNode, OutputNode, Slot
from apps.flow_new.serializers.nodes import BaseNodeSerializer, SlotSerializer


class InputNodeSerializer(BaseNodeSerializer):
    slots = SlotSerializer(many=True)

    class Meta(BaseNodeSerializer.Meta):
        model = InputNode
        fields = "__all__"

    def create(self, validated_data):
        if InputNode.objects.filter(flow=validated_data["flow"]).exists():
            raise serializers.ValidationError("InputNode already exists for this flow")

        slots = validated_data.pop("slots")

        for slot in slots:
            if slot["attachment_type"] != ATTACHMENT_TYPE.OUTPUT.value:
                raise serializers.ValidationError(
                    f"{slot['name']} - InputNode should have only output slots"
                )

        input_node = InputNode.objects.create(**validated_data)

        for slot in slots:
            Slot.objects.create(node=input_node, **slot)

        return input_node


class OutputNodeSerializer(BaseNodeSerializer):
    slots = SlotSerializer(many=True)

    class Meta(BaseNodeSerializer.Meta):
        model = OutputNode
        fields = "__all__"

    def create(self, validated_data):
        if OutputNode.objects.filter(flow=validated_data["flow"]).exists():
            raise serializers.ValidationError("OutputNode already exists for this flow")

        slots = validated_data.pop("slots")

        for slot in slots:
            if slot["attachment_type"] != ATTACHMENT_TYPE.INPUT.value:
                raise serializers.ValidationError(
                    f"{slot['name']} - Output Node should have only input slots"
                )

        output_node = OutputNode.objects.create(**validated_data)

        for slot in slots:
            Slot.objects.create(node=output_node, **slot)

        return output_node


class FlowNodeSerializer(BaseNodeSerializer):
    slots = SlotSerializer(many=True, read_only=True)

    class Meta(BaseNodeSerializer.Meta):
        model = FlowNode
        fields = "__all__"

    def validate(self, attrs):
        if attrs["represent"] == attrs["flow"]:
            raise serializers.ValidationError("FlowNode cannot represent itself")
        return super().validate(attrs)

    def create(self, validated_data):
        represent = validated_data.pop("represent")

        input_node = InputNode.objects.filter(flow=represent)
        output_node = OutputNode.objects.filter(flow=represent)

        input_slots = []
        output_slots = []

        if input_node.exists():
            input_slots = SlotSerializer(input_node[0].slots.all(), many=True).data

            for slot in input_slots:
                slot["attachment_type"] = ATTACHMENT_TYPE.INPUT.value

        if output_node.exists():
            output_slots = SlotSerializer(output_node[0].slots.all(), many=True).data

            for slot in output_slots:
                slot["attachment_type"] = ATTACHMENT_TYPE.OUTPUT.value

        slots = input_slots + output_slots

        flow_node = FlowNode.objects.create(represent=represent, **validated_data)

        for slot in slots:
            data = {
                "name": slot["name"],
                "attachment_type": slot["attachment_type"],
                "value_type": slot["value_type"],
            }
            Slot.objects.create(node=flow_node, **data)

        return flow_node
