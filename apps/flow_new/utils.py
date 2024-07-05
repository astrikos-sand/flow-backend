from apps.flow_new.enums import VALUE_TYPE


def default_position():
    return {"x": 0, "y": 0}


def typecast_value(value, type: str):
    match type:
        case VALUE_TYPE.INTEGER.value:
            return int(value)
        case VALUE_TYPE.STRING.value:
            return str(value)
        case VALUE_TYPE.BOOLEAN.value:
            return bool(value)
        case VALUE_TYPE.FLOAT.value:
            return float(value)
        case VALUE_TYPE.LIST.value:
            return list(value)
        case VALUE_TYPE.SET.value:
            return set(value)
        case VALUE_TYPE.TUPLE.value:
            return tuple(value)
        case VALUE_TYPE.DICTIONARY.value:
            return dict(value)
        case VALUE_TYPE.NONE.value:
            return None
        case VALUE_TYPE.ANY.value:
            return value
