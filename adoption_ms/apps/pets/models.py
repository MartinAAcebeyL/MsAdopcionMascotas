import logging
from typing import Union, List
from bson import ObjectId

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

    def get_a_pet(self, pet_id: str) -> Union[dict, None]:
        if not isinstance(pet_id, ObjectId):
            pet_id = ObjectId(pet_id)
        filter_criteria = {"_id": pet_id}
        pet = self.pets_collection.find_one(filter_criteria)

        if pet:
            pet["_id"] = str(pet["_id"])
            pet["person"]["_id"] = str(pet["person"]["_id"])

        return pet

    def get_pets_by_filters(self, *, filters: List) -> Union[List[any], None]:
        pets = list(self.pets_collection.find(filters))

        for pet in pets:
            if pet:
                pet["_id"] = str(pet["_id"])
                pet["person"]["_id"] = str(pet["person"]["_id"])

        return pets
