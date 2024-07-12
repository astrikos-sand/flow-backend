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

    # @classmethod
    # def get_node_fields(cls):
    #     return [
    #         {
    #             "type": "string",
    #             "key": ["definition", "name"],
    #             "placement": "node",
    #         },
    #         {
    #             "type": "string",
    #             "key": ["definition", "code"],
    #             "placement": "popup",
    #         },
    #     ]

    # @classmethod
    # def get_form_fields(cls):
    #     return [
    #         {
    #             "type": "select",
    #             "required": True,
    #             "label": "Definition",
    #             "choices": {
    #                 "key": ["name"],
    #                 "endpoint": "/definitions/",
    #                 "type": "list",
    #             },
    #         },
    #     ]