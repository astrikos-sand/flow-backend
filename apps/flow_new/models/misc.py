from django.db import models

from apps.flow_new.models.nodes import BaseNode, Slot
from apps.common.models import BaseModel


class DataNode(BaseNode):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=10000)

    def __str__(self):
        return f"{self.name} - {self.value}"

    # @classmethod
    # def get_node_fields(cls):
    #     return [
    #         {
    #             "type": "string",
    #             "key": ["name"],
    #             "placement": "node",
    #         },
    #         {
    #             "type": "string",
    #             "key": ["value"],
    #             "placement": "popup",
    #         },
    #     ]

    # @classmethod
    # def get_form_fields(cls):
    #     return [
    #         {
    #             "type": "input",
    #             "placeholder": "Name",
    #             "required": True,
    #             "reskey": ["name"],
    #         },
    #         {
    #             "type": "textarea",
    #             "placeholder": "Value",
    #             "required": True,
    #             "reskey": ["value"],
    #         },
    #     ]


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
    pass
