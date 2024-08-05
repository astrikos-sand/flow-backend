from enum import Enum

from django.db import models


class ITEM_TYPE(Enum):
    ARCHIVES = "archives"
    FUNCTION_DEFINITION = "function_definition"
    DEPENDENCY = "dependency"
    FLOW = "flow"
    PERIODIC_TRIGGER = "periodic"
    WEBHOOK_TRIGGER = "webhook"


class ATTACHMENT_TYPE(models.TextChoices):
    INPUT = "IN", "Input"
    OUTPUT = "OUT", "Output"


class VALUE_TYPE(models.TextChoices):
    INTEGER = "INT", "Integer"
    STRING = "STR", "String"
    BOOLEAN = "BOOL", "Boolean"
    FLOAT = "FLOAT", "Float"
    LIST = "LIST", "List"
    SET = "SET", "Set"
    TUPLE = "TUPLE", "Tuple"
    DICTIONARY = "DICT", "Dictionary"
    NONE = "NONE", "None"
    ANY = "ANY", "Any"


class NODE_COLOR_PALLETE(Enum):
    DATANODE = "#FFBB70"
    FUNCTION_NODE = "#CDE8E5"
    CONDITIONAL_NODE = "#E8C5E5"
    FOR_EACH_NODE = "#EEF7FF"
    FLOW_NODE = "#E6FF94"
    INPUT_NODE = "#F8DFD4"
    OUTPUT_NODE = "#B19470"
    BLOCK_NODE = "#FBF9F1"
