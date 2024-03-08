from pymongo.database import Database

from mongodb.utils import create_validator
from config.strings import MONGODB

resource_validator = create_validator(
    title=f"{MONGODB.resource} schema",
    properties={
        "resource_type": {"bsonType": "string"},
        "data": {"bsonType": "object"},
    },
    required=["resource_type", "data"],
)


def make_collections(db: Database):
    collections = db.list_collection_names()
    if "resource" not in collections:
        db.create_collection(
            MONGODB.resource,
            validator=resource_validator,
        )
