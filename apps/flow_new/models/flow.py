from django.db import models

from apps.flow_new.models.nodes import BaseNode
from apps.flow_new.models.base import Flow
from apps.flow_new.enums import NODE_COLOR_PALLETE


class InputNode(BaseNode):

    def __str__(self):
        return f"input node for {self.flow.name}"

    @classmethod
    def get_node_fields(cls):
        return {
            "color": NODE_COLOR_PALLETE.INPUT_NODE.value,
            "attrs": [
                {
                    "type": "id",
                    "placement": "popup",
                    "key": ["id"],
                }
            ],
        }

    @classmethod
    def get_form_fields(cls):
        return [
            {
                "type": "input",
                "placeholder": "Flow",
                "required": True,
                "label": "flow",
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
                            {"value": "OUT", "label": "Output"},
                        ],
                    },
                ],
            },
        ]


class OutputNode(BaseNode):

    def __str__(self):
        return f"output node for {self.flow.name}"

    @classmethod
    def get_node_fields(cls):
        return {
            "color": NODE_COLOR_PALLETE.OUTPUT_NODE.value,
            "attrs": [
                {
                    "type": "id",
                    "placement": "popup",
                    "key": ["id"],
                }
            ],
        }

    @classmethod
    def get_form_fields(cls):
        return [
            {
                "type": "input",
                "placeholder": "Flow",
                "required": True,
                "label": "flow",
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
                            {"value": "IN", "label": "Input"},
                        ],
                    },
                ],
            },
        ]


class FlowNode(BaseNode):
    represent = models.ForeignKey(
        Flow,
        on_delete=models.CASCADE,
        related_name="represent_nodes",
    )

    @classmethod
    def get_node_fields(cls):
        return {
            "color": NODE_COLOR_PALLETE.FLOW_NODE.value,
            "attrs": [
                {
                    "type": "span",
                    "label": "Target Flow Name",
                    "placement": "node",
                    "key": ["represent", "name"],
                },
                {
                    "type": "id",
                    "placement": "popup",
                    "key": ["id"],
                },
                {
                    "type": "link",
                    "placement": "popup",
                    "label": "Target Flow",
                    "key": ["represent", "id"],
                    "link_type": "flow",
                },
            ],
        }

    @classmethod
    def get_form_fields(cls):
        # TODO
        partial_flows = Flow.objects.all()
        choices = [
            {
                "value": flow.id,
                "label": flow.name,
            }
            for flow in partial_flows
        ]
        return [
            {
                "type": "input",
                "placeholder": "Flow",
                "required": True,
                "label": "flow",
            },
            {
                "type": "select",
                "placeholder": "Represent",
                "required": True,
                "label": "represent",
                "choices": choices,
            },
        ]
