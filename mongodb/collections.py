from pymongo.database import Database

from mongodb.utils import create_validator
from config.strings import MONGODB

resource_validator = create_validator(
    title=f"{MONGODB.resource} schema",
    properties={
        "data": {"bsonType": "object"},
    },
    required=["data"],
)


def make_collections(db: Database):
    collections = db.list_collection_names()
    if "resource" not in collections:
        db.create_collection(
            MONGODB.resource,
            validator=resource_validator,
        )
