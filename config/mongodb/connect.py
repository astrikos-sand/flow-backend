from pymongo import MongoClient

import config.const as const


def get_db():
    try:
        client = MongoClient(const.MONGO_URI)
        db = client[const.MONGO_DB]
        return db
    except:
        print("Error connecting to MongoDB")
        exit(1)
