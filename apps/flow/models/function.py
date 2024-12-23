from django.db import models

from apps.common.models import BaseModel
from apps.flow.enums import (
    ATTACHMENT_TYPE,
    VALUE_TYPE,
    NODE_COLOR_PALLETE,
)
from apps.flow.models.prefix import BaseModelWithPrefix
from apps.flow.models.nodes import BaseNode, Slot
from apps.flow.utils import function_upload_path
from config.storage import OverwriteStorage


class FunctionDefinition(BaseModelWithPrefix):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    code = models.FileField(upload_to=function_upload_path, storage=OverwriteStorage())
    doc_str = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.prefix:
            return f"{self.prefix.full_name}/{self.name}"
        return self.name

    @property
    def input_fields(self):
        return self.fields.filter(attachment_type=ATTACHMENT_TYPE.INPUT.value)

    @property
    def output_fields(self):
        return self.fields.filter(attachment_type=ATTACHMENT_TYPE.OUTPUT.value)

    @property
    def full_name(self):
        if self.prefix:
            return f"{self.prefix.full_name}/{self.name}"
        return self.name


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
        return f"{self.definition} ({self.flow})"

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
                    "label": "Code",
                    "key": ["definition", "code"],
                },
                {
                    "type": "p",
                    "placement": "popup",
                    "label": "Description",
                    "key": ["definition", "description"],
                },
                {
                    "type": "markdown",
                    "placement": "popup",
                    "label": "Doc String",
                    "key": ["definition", "doc_str"],
                },
            ],
        }

    @classmethod
    def get_form_fields(cls):
        function_definitions = FunctionDefinition.objects.all()

        definition_choices = [
            {
                "value": definition.id,
                "label": f"{definition.full_name}",
            }
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

    @property
    def datastore(self):
        input_slots = self.input_slots
        data = {}
        for slot in input_slots:
            try:
                default_dict = FunctionDataStore.objects.get(slot=slot)
                data[slot.name] = {
                    "value": default_dict.value,
                    "value_type": default_dict.value_type,
                }
            except FunctionDataStore.DoesNotExist:
                continue
        return data


class FunctionDataStore(BaseModel):
    slot = models.OneToOneField(
        Slot,
        on_delete=models.CASCADE,
    )
    value = models.CharField(max_length=10000)
    value_type = models.CharField(
        max_length=15,
        choices=VALUE_TYPE.choices,
    )

    def __str__(self):
        return f"{self.slot} - {self.value_type}"
