from apps.flow.enums import VALUE_TYPE
from ast import literal_eval


def default_position():
    return {"x": 0, "y": 0}


def typecast_value(value, data_type):
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


def function_upload_path(instance, _):
    function_name = instance.name
    if (
        instance.prefix
        and instance.prefix.full_name
        and instance.prefix.full_name.startswith("functions")
    ):
        return f"{instance.prefix.full_name}/{function_name}.py"
    return f"functions/miscellaneous/{function_name}.py"


def dependency_upload_path(instance, _):
    dependency_name = instance.name
    if (
        instance.prefix
        and instance.prefix.full_name
        and instance.prefix.full_name.startswith("environments")
    ):
        return f"{instance.prefix.full_name}/{dependency_name}.txt"

    return f"environments/miscellaneous/{dependency_name}.txt"


def archive_upload_path(instance, filename):
    if (
        instance.prefix
        and instance.prefix.full_name
        and instance.prefix.full_name.startswith("archives")
    ):
        return f"{instance.prefix.full_name}/{filename}"
    return f"archives/uploads/{filename}"
