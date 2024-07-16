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
    def get_node_fields(cls):
        return {
            "color": "#FF5733",
            "attrs": [
                {
                    "type": "span",
                    "placement": "node",
                    "key": ["name"],
                },
                {
                    "type": "id",
                    "placement": "popup",
                    "key": ["id"],
                },
                {
                    "type": "p",
                    "placement": "popup",
                    "key": ["value"],
                },
                {
                    "type": "span",
                    "placement": "popup",
                    "key": ["value_type"],
                },
            ],
        }

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
                "type": "input",
                "placeholder": "Flow",
                "required": True,
                "label": "flow",
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

    @property
    def name(self):
        return self.flow.name

    def __str__(self):
        return self.name


class ConditionalNode(BaseNode):
    value_type = models.CharField(
        max_length=15,
        choices=VALUE_TYPE.choices,
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_node_fields(cls):
        return {
            "color": "#FF5733",
            "attrs": [
                {
                    "type": "span",
                    "placement": "node",
                    "key": ["name"],
                },
                {
                    "type": "id",
                    "placement": "popup",
                    "key": ["id"],
                },
                {
                    "type": "list",
                    "key": ["cases"],
                    "placement": "node",
                    "child": [
                        {
                            "type": "span",
                            "key": ["name"],
                        },
                        {
                            "type": "scope",
                            "key": ["block", "id"],
                        },
                    ],
                },
                {
                    "type": "span",
                    "placement": "popup",
                    "key": ["value_type"],
                },
                {
                    "type": "list",
                    "key": ["cases"],
                    "placement": "popup",
                    "child": [
                        {
                            "type": "span",
                            "key": ["name"],
                        },
                        {
                            "type": "p",
                            "key": ["value"],
                        },
                    ],
                },
            ],
        }

    # TODO
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

    @property
    def name(self):
        return self.block.name

    def __str__(self):
        return self.name


class ForEachNode(BaseNode):
    block = models.OneToOneField(
        ScopeBlock,
        on_delete=models.CASCADE,
        related_name="for_each_node",
    )

    @property
    def name(self):
        return self.block.name

    def __str__(self):
        return self.name

    # TODO
    @classmethod
    def get_node_fields(cls):
        return {
            "color": "#FF5733",
            "attrs": [
                {
                    "type": "span",
                    "placement": "node",
                    "key": ["name"],
                },
                {
                    "type": "id",
                    "placement": "popup",
                    "key": ["id"],
                },
                {
                    "type": "scope",
                    "placement": "node",
                    "key": ["block", "id"],
                },
            ],
        }

    # TODO
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
