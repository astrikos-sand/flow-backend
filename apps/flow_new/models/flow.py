from django.db import models

from apps.flow_new.models.nodes import BaseNode
from apps.flow_new.models.base import Flow


class InputNode(BaseNode):
    pass


class OutputNode(BaseNode):
    pass


class FlowNode(BaseNode):
    represent = models.ForeignKey(
        Flow,
        on_delete=models.CASCADE,
        related_name="represent_nodes",
    )


class ScopeNode(BaseNode):
    represent = models.OneToOneField(
        Flow,
        on_delete=models.CASCADE,
        related_name="represent_scopes",
    )
