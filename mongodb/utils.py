def create_validator(
    title: str, properties: dict = {}, required: list[str] = []
) -> dict:
    json_schema = {
        "bsonType": "object",
        "title": title,
        "required": required,
        "properties": properties,
    }

    return {
        "$jsonSchema": json_schema,
        "additionalProperties": "false",
    }
