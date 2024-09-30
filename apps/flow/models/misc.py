from django.db import models

from apps.flow.models.nodes import BaseNode, Flow
from apps.flow.enums import ATTACHMENT_TYPE, VALUE_TYPE, NODE_COLOR_PALLETE
from apps.common.models import BaseModel


class DataNode(BaseNode):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=10000)
    value_type = models.CharField(
        max_length=15,
        choices=VALUE_TYPE.choices,
    )

    def __str__(self):
        return f"{self.name} ({self.flow})"

    def export_data(self):
        data = super().export_data()
        return {
            **data,
            "name": self.name,
            "value": self.value,
            "value_type": self.value_type,
            "node_type": "DataNode",
        }

    @classmethod
    def get_node_fields(cls):
        return {
            "color": NODE_COLOR_PALLETE.DATANODE.value,
            "attrs": [
                {
                    "type": "span",
                    "placement": "node",
                    "label": "name",
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
                    "label": "value",
                    "key": ["value"],
                },
                {
                    "type": "span",
                    "placement": "popup",
                    "label": "value_type",
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
        return self.name or "Conditional Node"

    @classmethod
    def get_node_fields(cls):
        return {
            "color": NODE_COLOR_PALLETE.CONDITIONAL_NODE.value,
            "attrs": [
                {
                    "type": "span",
                    "placement": "node",
                    "label": "name",
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
                    "label": "value_type",
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
                "type": "select",
                "placeholder": "Value Type",
                "required": True,
                "label": "value_type",
                "choices": [
                    {"value": choice[0], "label": choice[0]}
                    for choice in VALUE_TYPE.choices
                ],
            },
            {
                "type": "input",
                "placeholder": "Flow",
                "required": True,
                "label": "flow",
                "value": "",
            },
            {
                "type": "array",
                "label": "cases",
                "fields": [
                    {
                        "type": "input",
                        "placeholder": "Case Name",
                        "required": True,
                        "label": "name",
                    },
                    {
                        "type": "input",
                        "placeholder": "Case Value",
                        "required": True,
                        "label": "value",
                    },
                ],
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
                ],
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

    @classmethod
    def get_node_fields(cls):
        return {
            "color": NODE_COLOR_PALLETE.FOR_EACH_NODE.value,
            "attrs": [
                {
                    "type": "span",
                    "placement": "node",
                    "label": "name",
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
                "type": "input",
                "placeholder": "Flow",
                "required": True,
                "label": "flow",
                "value": "",
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
                ],
            },
        ]


class BlockNode(BaseNode):
    block = models.OneToOneField(
        ScopeBlock,
        on_delete=models.CASCADE,
        related_name="block_node",
    )

    @property
    def name(self):
        return self.block.name

    def __str__(self):
        return self.name

    @classmethod
    def get_node_fields(cls):
        return {
            "color": NODE_COLOR_PALLETE.BLOCK_NODE.value,
            "attrs": [
                {
                    "type": "span",
                    "placement": "node",
                    "label": "name",
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
                "type": "input",
                "placeholder": "Flow",
                "required": True,
                "label": "flow",
                "value": "",
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
                ],
            },
        ]
