from django.db import models

from apps.common.models import BaseModel
from apps.flow.enums import (
    ITEM_TYPE,
    ATTACHMENT_TYPE,
    VALUE_TYPE,
    NODE_COLOR_PALLETE,
)
from apps.flow.models.prefix import BaseModelWithPrefix
from apps.flow.models.nodes import BaseNode


class FunctionDefinition(BaseModelWithPrefix):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    code = models.FileField(upload_to="flow/functions/")

    def __str__(self):
        return f"{self.name}"

    @property
    def item_type(self) -> str:
        return ITEM_TYPE.FUNCTION_DEFINITION.value

    @property
    def input_fields(self):
        return self.fields.filter(attachment_type=ATTACHMENT_TYPE.INPUT.value)

    @property
    def output_fields(self):
        return self.fields.filter(attachment_type=ATTACHMENT_TYPE.OUTPUT.value)


class FunctionField(BaseModel):
    name = models.CharField(max_length=255)
    definition = models.ForeignKey(
        FunctionDefinition,
        on_delete=models.CASCADE,
        related_name="fields",
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
        return f"{self.name} - {self.definition}"

    class Meta:
        unique_together = ("name", "definition", "attachment_type")
        indexes = [
            models.Index(fields=["definition"]),
        ]


class FunctionNode(BaseNode):
    definition = models.ForeignKey(
        FunctionDefinition,
        on_delete=models.CASCADE,
        related_name="nodes",
    )

    def __str__(self):
        return f"{self.definition} - {self.flow}"

    def export_data(self):
        data = super().export_data()
        return {
            **data,
            "definition": self.definition.id,
            "node_type": "FunctionNode",
        }

    @classmethod
    def get_node_fields(cls):
        return {
            "color": NODE_COLOR_PALLETE.FUNCTION_NODE.value,
            "attrs": [
                {
                    "type": "span",
                    "label": "Function",
                    "placement": "node",
                    "key": ["definition", "name"],
                },
                {
                    "type": "id",
                    "placement": "popup",
                    "key": ["id"],
                },
                {
                    "type": "link",
                    "placement": "popup",
                    "label": "Definition",
                    "key": ["definition", "id"],
                    "link_type": "function_definition",
                },
                {
                    "type": "link",
                    "placement": "popup",
                    "label": "Code",
                    "key": ["definition", "code"],
                },
            ],
        }

    @classmethod
    def get_form_fields(cls):
        function_definitions = FunctionDefinition.objects.all()

        definition_choices = [
            {"value": definition.id, "label": definition.name}
            for definition in function_definitions
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
                "placeholder": "Definition",
                "required": True,
                "label": "definition",
                "choices": definition_choices,
            },
        ]
