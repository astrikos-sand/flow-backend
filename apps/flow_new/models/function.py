from django.db import models

from apps.common.models import BaseModel
from apps.flow_new.enums import ITEM_TYPE, ATTACHMENT_TYPE, VALUE_TYPE
from apps.flow_new.models.base import BaseModelWithTag
from apps.flow_new.models.nodes import BaseNode


class FunctionDefinition(BaseModelWithTag):
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
                "placeholder": "Code",
                "required": True,
                "label": "code",
            },
            {
                "type": "input",
                "placeholder": "Field Name",
                "required": True,
                "label": "fields.name",
            },
            {
                "type": "select",
                "placeholder": "Attachment Type",
                "required": True,
                "label": "fields.attachment_type",
                "choices": ["IN", "OUT"],
            },
        ]


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
