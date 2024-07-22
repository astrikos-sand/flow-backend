from apps.flow_new.enums import VALUE_TYPE
from ast import literal_eval


def default_position():
    return {"x": 0, "y": 0}


def typecast_value(data_type, value):
    match data_type:
        case VALUE_TYPE.INTEGER.value:
            return int(value)

        case VALUE_TYPE.STRING.value:
            return str(value)

        case VALUE_TYPE.BOOLEAN.value:
            return bool(value)

        case VALUE_TYPE.FLOAT.value:
            return float(value)

        case VALUE_TYPE.LIST.value:
            value = literal_eval(value)
            if type(value) is not list:
                raise f"Invalid type of data node, given list but got {type(value)}"
            return value

        case VALUE_TYPE.SET.value:
            value = literal_eval(value)
            if type(value) is not set:
                raise f"Invalid type of data node, given set but got {type(value)}"
            return value

        case VALUE_TYPE.TUPLE.value:
            value = literal_eval(value)
            if type(value) is not tuple:
                raise f"Invalid type of data node, given tuple but got {type(value)}"
            return value

        case VALUE_TYPE.DICTIONARY.value:
            value = literal_eval(value)
            if type(value) is not dict:
                raise f"Invalid type of data node, given dict but got {type(value)}"
            return value

        case VALUE_TYPE.NONE.value:
            return None

        case VALUE_TYPE.ANY.value:
            return value
