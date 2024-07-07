from django.db import models

from apps.flow_new.models.nodes import BaseNode, Slot
from apps.common.models import BaseModel


class DataNode(BaseNode):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=10000)

    def __str__(self):
        return f"{self.name} - {self.value}"


class ConditionalNodeValue(BaseModel):
    value = models.CharField(max_length=255)
    slot = models.OneToOneField(
        Slot,
        on_delete=models.CASCADE,
        related_name="conditional_node_value",
    )

    def __str__(self):
        return f"{self.value} - {self.slot}"


class ConditionalNode(BaseNode):
    pass


class ForEachNode(BaseNode):
    # TODO: It will have single input slot as list and
    # single output slot as element of the list
    pass
