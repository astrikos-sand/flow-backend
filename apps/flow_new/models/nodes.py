from django.core.exceptions import ValidationError
from django.db import models

from polymorphic.models import PolymorphicModel

from apps.common.models import BaseModel
from apps.flow_new.utils import default_position
from apps.flow_new.enums import ATTACHMENT_TYPE, VALUE_TYPE
from apps.flow_new.models.base import Flow

# TODO: Add unique constraint at the serializer level
# TODO: Use serializer to validate the data


class BaseNode(BaseModel, PolymorphicModel):
    position = models.JSONField(default=default_position)
    flow = models.ForeignKey(
        Flow,
        on_delete=models.CASCADE,
        related_name="nodes",
    )

    class Meta:
        indexes = [
            models.Index(fields=["flow"]),
        ]

    @property
    def input_slots(self):
        return self.slots.filter(attachment_type=ATTACHMENT_TYPE.INPUT.value)

    @property
    def output_slots(self):
        return self.slots.filter(attachment_type=ATTACHMENT_TYPE.OUTPUT.value)

    @property
    def connections_in(self):
        connections = []
        for slot in self.input_slots:
            connections.extend(Connection.objects.filter(to_slot=slot))
        return connections

    @property
    def connections_out(self):
        connections = []
        for slot in self.output_slots:
            connections.extend(Connection.objects.filter(from_slot=slot))
        return connections

    @classmethod
    def get_node_fields(cls):
        raise NotImplementedError

    @classmethod
    def get_form_fields(cls):
        raise NotImplementedError

    def export_data(self):
        return {
            "position": self.position,
            "input_slots": self.input_slots,
            "output_slots": self.output_slots,
            "connections_in": self.connections_in,
            "connections_out": self.connections_out,
        }


# TODO: rm the value type from slot
class Slot(BaseModel):
    name = models.CharField(max_length=255)
    node = models.ForeignKey(
        BaseNode,
        on_delete=models.CASCADE,
        related_name="slots",
    )
    attachment_type = models.CharField(
        max_length=10,
        choices=ATTACHMENT_TYPE.choices,
    )
    value_type = models.CharField(
        max_length=15,
        choices=VALUE_TYPE.choices,
        default=VALUE_TYPE.ANY,
    )

    def __str__(self):
        return f"{self.name} - {self.node}"

    class Meta:
        unique_together = ("name", "node", "attachment_type")
        indexes = [
            models.Index(fields=["node"]),
        ]


class Connection(BaseModel):
    from_slot = models.ForeignKey(
        Slot, on_delete=models.CASCADE, related_name="connections_out"
    )
    to_slot = models.ForeignKey(
        Slot, on_delete=models.CASCADE, related_name="connections_in"
    )

    def __str__(self):
        return f"{self.from_slot} -> {self.to_slot}"

    def clean(self) -> None:
        if str(self.from_slot.node.id) == str(self.to_slot.node.id):
            raise ValidationError("Cannot create connection bw slots in the same node")

        if str(self.from_slot.node.flow.id) != str(self.to_slot.node.flow.id):
            raise ValidationError(
                "Cannot create connection bw slots in different flows"
            )

        if self.from_slot.attachment_type != ATTACHMENT_TYPE.OUTPUT.value:
            raise ValidationError("Cannot create connection from input slot")

        if self.to_slot.attachment_type != ATTACHMENT_TYPE.INPUT.value:
            raise ValidationError("Cannot create connection to output slot")

        return super().clean()

    def save(
        self,
        **kwargs,
    ) -> None:
        self.full_clean()
        return super().save(**kwargs)

    class Meta:
        unique_together = ("from_slot", "to_slot")
