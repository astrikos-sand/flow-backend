from django.db import models

from apps.flow_new.models.nodes import BaseNode


class DataNode(BaseNode):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=10000)

    # TODO: save the type in the output slot

    def __str__(self):
        return f"{self.name} - {self.value}"


class ConditionalNode(BaseNode):
    # TODO: It will have single input slot as condition and multiple output slots
    pass


class ForEachNode(BaseNode):
    # TODO: It will have single input slot as list and
    # single output slot as element of the list
    pass
