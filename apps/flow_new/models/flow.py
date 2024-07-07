from django.db import models

from apps.flow_new.models.nodes import BaseNode
from apps.flow_new.models.base import Flow


class InputNode(BaseNode):
    # TODO: create the output slots
    pass


class OutputNode(BaseNode):
    # TODO: create the input slots
    pass


class FlowNode(BaseNode):
    represent = models.ForeignKey(
        Flow,
        on_delete=models.CASCADE,
        related_name="represent_nodes",
    )

    # TODO: create the input and output slots based on the input
    # and output node of the flow
