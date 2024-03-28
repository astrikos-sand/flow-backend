from django.db import models

from apps.common.models import BaseModel
from apps.flow.models import GenericNode


class WebHookEvent(BaseModel):
    trigger_node = models.ForeignKey(GenericNode, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.name} ( {self.description} ) [Trigger Node: {self.trigger_node.id}]"
        )
