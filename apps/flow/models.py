from django.db import models

from polymorphic.models import PolymorphicModel

from apps.common.models import BaseModel


class FlowFile(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ( {self.description} )"


class DynamicNodeClass(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    code = models.FileField(upload_to="flow/node_classes/")

    def execute(self, globals, locals):
        exec(self.code.read(), globals, locals)
        return locals

    def __str__(self):
        return f"{self.name} ( {self.description} ) [Code: {self.code.name}]"


class Slot(BaseModel):

    class ATTACHMENT_TYPE(models.TextChoices):
        INPUT = "IN", "Input"
        OUTPUT = "OUT", "Output"

    name = models.CharField(max_length=100)
    attachment_type = models.CharField(choices=ATTACHMENT_TYPE.choices, max_length=5)
    node_class = models.ForeignKey(
        DynamicNodeClass, on_delete=models.CASCADE, related_name="slots"
    )


class BaseNode(BaseModel, PolymorphicModel):
    flow_file = models.ForeignKey(
        FlowFile, on_delete=models.CASCADE, related_name="nodes"
    )

    @property
    def input_slots(self):
        return []

    @property
    def output_slots(self):
        return []

    def execute(self, globals, locals):
        return locals

    def __str__(self):
        return f"{self.id} [Flow: {self.flow_file.name}]"


class DynamicNode(BaseNode):
    node_class = models.ForeignKey(
        DynamicNodeClass, on_delete=models.CASCADE, related_name="nodes"
    )

    def execute(self, globals, locals):
        self.node_class.execute(globals, locals)
        if not all(slot in locals for slot in self.output_slots):
            raise ValueError(
                "Slot is not found in function output, check values returned by function"
            )
        return locals

    def input_slots(self):
        return self.node_class.slots.filter(
            attachment_type=Slot.ATTACHMENT_TYPE.INPUT
        ).values_list("name", flat=True)

    def output_slots(self):
        return self.node_class.slots.filter(
            attachment_type=Slot.ATTACHMENT_TYPE.OUTPUT
        ).value_list("name", flat=True)

    def __str__(self):
        return f"{super().__str__()} [Node Class: {self.node_class.name}]"


class DataNode(BaseNode):

    class DATA_TYPE(models.TextChoices):
        INTEGER = "INT", "Integer"
        STRING = "STR", "String"
        BOOLEAN = "BOOL", "Boolean"
        FLOAT = "FLOAT", "Float"
        LIST = "LIST", "List"
        SET = "SET", "Set"
        TUPLE = "TUPLE", "Tuple"
        DICTIONARY = "DICT", "Dictionary"

    value = models.CharField(max_length=255)
    type = models.CharField(choices=DATA_TYPE.choices, max_length=5)

    @property
    def input_slots(self):
        return []

    def output_slots(self):
        return ["data"]

    def get_data(self):
        match self.type:
            case self.DATA_TYPE.INTEGER:
                return int(self.value)
            case self.DATA_TYPE.STRING:
                return str(self.value)
            case self.DATA_TYPE.BOOLEAN:
                return bool(self.value)
            case self.DATA_TYPE.FLOAT:
                return float(self.value)
            case self.DATA_TYPE.LIST:
                return list(self.value)
            case self.DATA_TYPE.SET:
                return set(self.value)
            case self.DATA_TYPE.TUPLE:
                return tuple(self.value)
            case self.DATA_TYPE.DICTIONARY:
                return dict(self.value)
            case default:
                return None

    def execute(self, globals, locals):
        locals["data"] = self.get_data()
        return locals
    
    def __str__(self):
        return f"{super().__str__()} [Value: {self.value}]"


class Connection(BaseModel):
    source = models.ForeignKey(
        BaseNode, on_delete=models.CASCADE, related_name="source_connections"
    )

    target = models.ForeignKey(
        BaseNode, on_delete=models.CASCADE, related_name="target_connections"
    )

    source_slot = models.CharField(max_length=255)
    target_slot = models.CharField(max_length=255)

    def __str__(self):
        return (
            f"{self.source} [{self.source_slot}] -> {self.target} [{self.target_slot}]"
        )

    # Validate that the source and target are not the same
    # Validate that the source parameter belong to the source node's output slot
    # Validate that the target parameter belong to the target node's input slot

    class Meta:
        unique_together = ("source", "target")
