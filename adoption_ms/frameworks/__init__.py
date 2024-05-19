from .db.mongo import MongoConnection

mongo_client = MongoConnection()

__all__ = ["mongo_client"]
