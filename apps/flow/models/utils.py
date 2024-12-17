from django.db import models

from apps.common.models import BaseModel
from apps.flow.models.flow import Flow


class DAGMetaData(BaseModel):
    flow = models.OneToOneField(
        Flow,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    config = models.JSONField(default=dict)
