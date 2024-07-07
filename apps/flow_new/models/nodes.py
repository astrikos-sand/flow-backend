from django.db import models

from polymorphic.models import PolymorphicModel

from apps.common.models import BaseModel
from apps.flow_new.utils import default_position
from apps.flow_new.enums import ATTACHMENT_TYPE, VALUE_TYPE
from apps.flow_new.models.base import Flow


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
            raise ValueError("Cannot create connection bw slots in the same node")
        return super().clean()

    class Meta:
        unique_together = ("from_slot", "to_slot")
