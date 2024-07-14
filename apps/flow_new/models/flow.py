from django.db import models

from apps.flow_new.models.nodes import BaseNode
from apps.flow_new.models.base import Flow


class InputNode(BaseNode):

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
                        "choices": ["OUT"],
                    },
                ],
            },
        ]


class OutputNode(BaseNode):
    # Other fields and methods

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
                        "choices": ["IN"],
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
    def get_form_fields(cls):
        return [
            {
                "type": "input",
                "placeholder": "Flow",
                "required": True,
                "label": "flow",
            },
            {
                "type": "input",
                "placeholder": "Represent",
                "required": True,
                "label": "represent",
            },
        ]
