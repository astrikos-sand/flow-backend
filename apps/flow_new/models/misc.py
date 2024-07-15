from django.db import models

from apps.flow_new.models.nodes import BaseNode, Flow
from apps.flow_new.enums import ATTACHMENT_TYPE, VALUE_TYPE
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

    @classmethod
    def get_form_fields(cls):
        return [
            {
                "type": "input",
                "placeholder": "Name",
                "required": True,
                "label": "name",
            },
            {
                "type": "textarea",
                "placeholder": "Value",
                "required": True,
                "label": "value",
            },
            {
                "type": "select",
                "placeholder": "Value Type",
                "required": True,
                "label": "value_type",
                "choices": [
                    {"value": choice[0], "label": choice[0]}
                    for choice in VALUE_TYPE.choices
                ],
            },
        ]


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

    @classmethod
    def get_form_fields(cls):
        return [
            {
                "type": "input",
                "placeholder": "Name",
                "required": True,
                "label": "name",
            },
            {
                "type": "array",
                "label": "slots",
                "fields": [
                    {
                        "type": "input",
                        "placeholder": "Slot Name",
                        "required": True,
                        "label": "name",
                    },
                    {
                        "type": "select",
                        "placeholder": "Attachment Type",
                        "required": True,
                        "label": "attachment_type",
                        "choices": [
                            {"value": choice[0], "label": choice[0]}
                            for choice in ATTACHMENT_TYPE.choices
                        ],
                    },
                    {
                        "type": "select",
                        "placeholder": "Value Type",
                        "required": True,
                        "label": "value_type",
                        "choices": [
                            {"value": choice[0], "label": choice[0]}
                            for choice in VALUE_TYPE.choices
                        ],
                    },
                ],
            },
            {
                "type": "textarea",
                "placeholder": "Slot Values",
                "required": False,
                "label": "values",
            },
        ]


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

    @classmethod
    def get_form_fields(cls):
        return [
            {
                "type": "input",
                "placeholder": "Name",
                "required": True,
                "reskey": ["name"],
            },
            {
                "type": "textarea",
                "placeholder": "Value",
                "required": True,
                "reskey": ["value"],
            },
        ]
