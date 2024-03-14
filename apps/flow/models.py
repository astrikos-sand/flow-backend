from django.db import models

from polymorphic.models import PolymorphicModel

from apps.common.models import BaseModel


class FlowFile(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ( {self.description} )"


class NodeClass(BaseModel, PolymorphicModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def execute(self, globals, locals):
        return locals

    def __str__(self):
        return f"{self.name} ( {self.description} )"


class DynamicNodeClass(NodeClass):
    code = models.FileField(upload_to="flow/node_classes/")

    def execute(self, globals, locals):
        exec(self.code.read(), globals, locals)
        return locals
    
    def __str__(self):
        return f"{self.name} ( {self.description} ) [Code: {self.code.name}]"


class DataNodeClass(NodeClass):
    class DATA_TYPE(models.TextChoices):
        INTEGER = "INT", "Integer"
        STRING = "STR", "String"
        BOOLEAN = "BOOL", "Boolean"

    value = models.CharField(max_length=255)
    type = models.CharField(choices=DATA_TYPE.choices, max_length=10)

    def get_data(self):
        match self.type:
            case "INT":
                return int(self.value)
            case "STR":
                return str(self.value)
            case "BOOL":
                return bool(self.value)
            case default:
                return None

    def execute(self, globals, locals):
        data = self.get_data()
        locals.update({self.name: data})
        return locals
    
    def __str__(self):
        return f"{self.name} ( {self.description} ) [value: {self.get_data()}]"


class Node(BaseModel):
    flow_file = models.ForeignKey(
        FlowFile, on_delete=models.CASCADE, related_name="nodes"
    )
    node_class = models.ForeignKey(
        NodeClass, on_delete=models.CASCADE, related_name="nodes"
    )

    def __str__(self):
        return f"{self.id} [Flow: {self.flow_file.name}] [Node Class: {self.node_class.name}]"


class Parameter(BaseModel):

    class BEHAVIOUR(models.TextChoices):
        INPUT = "IN", "Input"
        OUTPUT = "OUT", "Output"

    name = models.CharField(max_length=100)
    node_class = models.ForeignKey(
        NodeClass, on_delete=models.CASCADE, related_name="parameters"
    )
    description = models.TextField(null=True, blank=True)
    behaviour = models.CharField(choices=BEHAVIOUR.choices, max_length=10)

    class Meta:
        unique_together = ("name", "node_class")

    def __str__(self):
        return (
            f"{self.name} ( {self.description} ) [Node Class: {self.node_class.name}]"
        )


class Connections(BaseModel):
    source = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="source_connections"
    )
    target = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="target_connections"
    )
    source_parameter = models.ForeignKey(
        Parameter,
        default=None,
        on_delete=models.CASCADE,
        related_name="source_connections",
    )
    target_parameter = models.ForeignKey(
        Parameter,
        default=None,
        on_delete=models.CASCADE,
        related_name="target_connections",
    )

    # Validate that the source and target are not the same
    # Validate that the source parameter belong to the source node's node class
    # Validate that the target parameter belong to the target node's node class
    # Validate that source parameter is OUTPUT and target parameter is INPUT
    # Validate that target can't be a DataNodeClass
    class Meta:
        unique_together = ("source", "target")

    def __str__(self):
        return f"{self.source.node_class.name} -> {self.target.node_class.name}"
