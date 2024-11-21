from rest_framework import serializers

from apps.flow.enums import ATTACHMENT_TYPE

from apps.flow.models import FlowNode, InputNode, OutputNode, Slot, Flow, ScopeBlock

from apps.flow.serializers.nodes import (
    BaseNodeSerializer,
    SlotSerializer,
    ConnectionSerializer,
)

from apps.flow.serializers.prefix import FlowSerializer


class InputNodeSerializer(BaseNodeSerializer):
    slots = SlotSerializer(many=True, write_only=True)

    class Meta(BaseNodeSerializer.Meta):
        model = InputNode

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
    slots = SlotSerializer(many=True, write_only=True)

    class Meta(BaseNodeSerializer.Meta):
        model = OutputNode

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
    name = serializers.CharField(read_only=True)

    class Meta(BaseNodeSerializer.Meta):
        model = FlowNode

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["represent"] = FlowSerializer(instance.represent).data
        return data

    def create(self, validated_data):
        if validated_data["represent"] == validated_data["flow"]:
            raise serializers.ValidationError("FlowNode cannot represent itself")

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


class ScopeSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True, write_only=True)
    name = serializers.CharField(write_only=True)
    scope = serializers.PrimaryKeyRelatedField(
        queryset=Flow.objects.all(), write_only=True
    )
    flow = FlowSerializer(read_only=True)

    class Meta:
        model = ScopeBlock
        exclude = (
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        slots = validated_data.pop("slots")

        input_slots = [
            slot
            for slot in slots
            if slot["attachment_type"] == ATTACHMENT_TYPE.INPUT.value
        ]

        output_slots = [
            {**slot, "attachment_type": ATTACHMENT_TYPE.OUTPUT.value}
            for slot in input_slots
        ]

        slots = input_slots + output_slots

        flow_data = {
            "name": validated_data.pop("name"),
            "scope": validated_data.pop("scope").id,
        }

        flow_serializer = FlowSerializer(data=flow_data)
        flow_serializer.is_valid(raise_exception=True)
        flow_serializer.save()

        flow = flow_serializer.instance

        input_node_serializer = InputNodeSerializer(
            data={"flow": flow.id, "slots": output_slots}
        )
        input_node_serializer.is_valid(raise_exception=True)
        input_node_serializer.save()

        input_node = input_node_serializer.instance

        output_node_serializer = OutputNodeSerializer(
            data={"flow": flow.id, "slots": input_slots}
        )
        output_node_serializer.is_valid(raise_exception=True)
        output_node_serializer.save()

        output_node = output_node_serializer.instance

        input_node_slots = input_node.output_slots
        output_node_slots = output_node.input_slots

        data = [
            {
                "from_slot": input_node_slot.id,
                "to_slot": output_node_slot.id,
            }
            for input_node_slot, output_node_slot in zip(
                input_node_slots, output_node_slots
            )
        ]

        connection_serializer = ConnectionSerializer(data=data, many=True)
        connection_serializer.is_valid(raise_exception=True)
        connection_serializer.save()

        scope_block = ScopeBlock.objects.create(flow=flow)

        return scope_block
