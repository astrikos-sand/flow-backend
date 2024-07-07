from enum import Enum

from django.db import models


class ITEM_TYPE(Enum):
    ARCHIVES = "archives"
    FUNCTION_DEFINITION = "function_definition"
    DEPENDENCY = "dependency"
    FLOW = "flow"


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
