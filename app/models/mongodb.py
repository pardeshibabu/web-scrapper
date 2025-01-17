from pymongo import MongoClient
from app.config import MONGO_URI, MONGO_DB_NAME

class MongoDBModel:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]
