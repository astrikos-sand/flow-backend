from pymongo import MongoClient
from pymongo.database import Database

import config.const as const


class Mongo:
    def __init__(self):
        self.client = self.get_client(const.MONGO_URI)
        self.db = self.get_db(const.MONGO_DB)

    def get_db(self, db_name: str) -> Database:
        return self.client[db_name]

    def get_client(self, URI: str) -> MongoClient:
        try:
            client = MongoClient(URI)
            return client
        except:
            print("Error connecting to MongoDB")
            exit(1)

    def ensure_connection(self):
        try:
            self.client.server_info()
        except:
            print("Error connecting to MongoDB")
            exit(1)
