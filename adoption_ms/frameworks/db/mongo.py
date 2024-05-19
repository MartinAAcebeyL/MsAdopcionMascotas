import os
from pymongo import MongoClient


class MongoConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoConnection, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, *args, **kwargs):
        self.client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = self.client["adoptionMs"]

    def get_collection(self, collection: str):
        return self.db[collection]
