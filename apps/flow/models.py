from django.db import models
from django.db.models import Max, F
import json

from polymorphic.models import PolymorphicModel

from apps.common.models import BaseModel
from apps.flow.utils import default_position


class FlowFile(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    environment = models.ForeignKey(
        "Environment",
        related_name="flow_files",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.name} ( {self.description} )"


class Environment(BaseModel):
    name = models.CharField(max_length=100)
    requirements = models.FileField(upload_to="flow/environments/")

    def __str__(self):
        return f"{self.name}"


class BaseNodeClass(BaseModel, PolymorphicModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    code = models.FileField(upload_to="flow/node_classes/")

    def execute(self, globals, locals):
        with self.code.open() as file:
            code_text = file.read()
        exec(code_text, globals, locals)
        return locals

    @property
    def input_slots(self):
        return list(
            self.slots.filter(
                attachment_type=Slot.ATTACHMENT_TYPE.INPUT,
                speciality=Slot.SPECIAL_SLOT.NONE,
            ).values_list("name", flat=True)
        )

    @property
    def output_slots(self):
        return list(
            self.slots.filter(
                attachment_type=Slot.ATTACHMENT_TYPE.OUTPUT,
                speciality=Slot.SPECIAL_SLOT.NONE,
            ).values_list("name", flat=True)
        )

    @property
    def delayed_output_slots(self):
        return list(
            self.slots.filter(
                attachment_type=Slot.ATTACHMENT_TYPE.DELAYED_OUTPUT,
                speciality=Slot.SPECIAL_SLOT.NONE,
            ).values_list("name", flat=True)
        )

    @property
    def special_slots(self):
        return list(
            self.slots.exclude(speciality=Slot.SPECIAL_SLOT.NONE)
            .exclude(attachment_type=Slot.ATTACHMENT_TYPE.DELAYED_OUTPUT)
            .values("name", "speciality", "attachment_type")
        )

    @property
    def special_input_slots(self):
        return list(
            self.slots.filter(attachment_type=Slot.ATTACHMENT_TYPE.INPUT)
            .exclude(speciality=Slot.SPECIAL_SLOT.NONE)
            .values_list("name", flat=True)
        )

    @property
    def special_output_slots(self):
        return list(
            self.slots.filter(attachment_type=Slot.ATTACHMENT_TYPE.OUTPUT)
            .exclude(speciality=Slot.SPECIAL_SLOT.NONE)
            .values_list("name", flat=True)
        )

    @property
    def delayed_special_output_slots(self):
        return list(
            self.slots.filter(attachment_type=Slot.ATTACHMENT_TYPE.DELAYED_OUTPUT)
            .exclude(speciality=Slot.SPECIAL_SLOT.NONE)
            .values("name", "speciality", "attachment_type")
        )

    def __str__(self):
        return f"{self.name} ( {self.description} ) [Code: {self.code.name}]"


class GenericNodeClass(BaseNodeClass):

    @classmethod
    def get_allowed_attachment_types(cls):
        allwed_list = Slot.ATTACHMENT_TYPE.values.copy()
        allwed_list.remove(Slot.ATTACHMENT_TYPE.DELAYED_OUTPUT)
        return allwed_list


class TriggerNodeClass(BaseNodeClass):

    @classmethod
    def get_attachment_types(cls):
        allwed_list = Slot.ATTACHMENT_TYPE.values.copy()
        return allwed_list


class Slot(BaseModel):

    class ATTACHMENT_TYPE(models.TextChoices):
        INPUT = "IN", "Input"
        OUTPUT = "OUT", "Output"
        DELAYED_OUTPUT = "D_OUT", "Delayed Output"

    class SPECIAL_SLOT(models.TextChoices):
        DATABASE = "DB", "Database"
        API = "API", "API"
        BACKEND = "BACKEND", "Backend"
        NODE_ID = "NODE_ID", "Node ID"
        NONE = "NONE", "None"
        SIGNAL = "SIG", "Signal"

    name = models.CharField(max_length=100)
    attachment_type = models.CharField(choices=ATTACHMENT_TYPE.choices, max_length=5)
    node_class = models.ForeignKey(
        BaseNodeClass, on_delete=models.CASCADE, related_name="slots"
    )
    speciality = models.CharField(
        choices=SPECIAL_SLOT.choices, max_length=10, default=SPECIAL_SLOT.NONE
    )

    class Meta:
        unique_together = ("name", "node_class")

    def __str__(self):
        return f"{self.name} [Attachment: {self.attachment_type}] [Node Class: {self.node_class.name}]"


class BaseNode(BaseModel, PolymorphicModel):
    flow_file = models.ForeignKey(
        FlowFile, on_delete=models.CASCADE, related_name="nodes"
    )
    position = models.JSONField(default=default_position)

    @property
    def input_slots(self):
        return []

    @property
    def output_slots(self):
        return []

    @property
    def special_slots(self):
        return []

    @property
    def special_input_slots(self):
        return []

    @property
    def special_output_slots(self):
        return []

    @property
    def delayed_output_slots(self):
        return []

    @property
    def delayed_special_output_slots(self):
        return []

    @property
    def outputs(self):
        outputs = self.results.first().outputs
        return outputs

    @property
    def inputs(self):
        inputs = self.results.first().inputs
        return inputs

    def execute(self, globals, locals):
        return locals

    def __str__(self):
        return f"{self.id} [Flow: {self.flow_file.name}]"


class GenericNode(BaseNode):
    node_class = models.ForeignKey(
        BaseNodeClass, on_delete=models.CASCADE, related_name="nodes"
    )

    def execute(self, globals, locals):
        self.node_class.execute(globals, locals)
        outputs = {}
        # for slot in self.output_slots:
        #     if slot in locals:
        #         outputs.update({slot: locals[slot]})
        #     else:
        #         raise ValueError(
        #             "Slot is not found in function output, check values returned by function"
        #         )
        return outputs

    @property
    def input_slots(self):
        return self.node_class.input_slots

    @property
    def output_slots(self):
        return self.node_class.output_slots

    @property
    def special_slots(self):
        return self.node_class.special_slots

    @property
    def special_input_slots(self):
        return self.node_class.special_input_slots

    @property
    def special_output_slots(self):
        return self.node_class.special_output_slots

    @property
    def delayed_output_slots(self):
        return self.node_class.delayed_output_slots

    @property
    def delayed_special_output_slots(self):
        return self.node_class.delayed_special_output_slots

    @property
    def node_class_type(self):
        return self.node_class.get_real_instance_class().__name__

    @property
    def node_class_name(self):
        return self.node_class.name

    @property
    def code(self):
        return self.node_class.code

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
        NONE = "NONE", "None"

    value = models.CharField(max_length=255)
    type = models.CharField(choices=DATA_TYPE.choices, max_length=5)

    @property
    def input_slots(self):
        return []

    @property
    def output_slots(self):
        return ["data"]

    @property
    def special_slots(self):
        return []

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
        outputs = {}
        outputs["data"] = self.get_data()
        return outputs

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
        unique_together = ("source", "target", "source_slot", "target_slot")


class NodeResult(BaseModel):
    node = models.ForeignKey(BaseNode, on_delete=models.CASCADE, related_name="results")
    outputs = models.JSONField(null=True, blank=True, default=dict)
    inputs = models.JSONField(null=True, blank=True, default=dict)
