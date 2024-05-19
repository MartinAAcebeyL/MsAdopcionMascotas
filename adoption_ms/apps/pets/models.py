from frameworks import mongo_client

class Pet:
    @classmethod
    def get_all_users(cls):
        users_collection = mongo_client.get_collection("users")
        all_users = list(users_collection.find({}))
        return all_users
