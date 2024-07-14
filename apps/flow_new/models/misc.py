from django.db import models

from apps.flow_new.models.nodes import BaseNode, Slot, Flow
from apps.flow_new.enums import VALUE_TYPE
from apps.common.models import BaseModel


class DataNode(BaseNode):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=10000)
    value_type = models.CharField(
        max_length=15,
        choices=VALUE_TYPE.choices,
    )

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


class ScopeBlock(BaseModel):
    flow = models.OneToOneField(
        Flow,
        on_delete=models.CASCADE,
        related_name="scope_block",
    )

    def __str__(self):
        return self.flow.name


class ConditionalNode(BaseNode):
    value_type = models.CharField(
        max_length=15,
        choices=VALUE_TYPE.choices,
    )


class ConditionalNodeCase(BaseModel):
    value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    block = models.OneToOneField(
        ScopeBlock,
        on_delete=models.CASCADE,
        related_name="conditional_node_case",
    )
    node = models.ForeignKey(
        ConditionalNode,
        on_delete=models.CASCADE,
        related_name="cases",
    )


class ForEachNode(BaseNode):
    block = models.OneToOneField(
        ScopeBlock,
        on_delete=models.CASCADE,
        related_name="for_each_node",
    )
