import logging
from frameworks import mongo_client


class Pet:
    def __init__(self) -> None:
        self.pets_collection = mongo_client.get_collection("pets")

    @classmethod
    def get_all_users(cls):
        users_collection = mongo_client.get_collection("users")
        all_users = list(users_collection.find({}))
        return all_users

    def save_a_pet(self, pet: dict):
        try:
            new_pet = self.pets_collection.insert_one(pet)
            return new_pet.inserted_id
        except Exception as e:
            logging.error(f"An error occurred while saving the pet: {e}")
            return None
