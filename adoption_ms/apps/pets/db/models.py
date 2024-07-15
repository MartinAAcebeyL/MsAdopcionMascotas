import logging
from typing import Union, List, Tuple
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

    @classmethod
    def get_a_user_by_google_id(cls, id: str):
        users_collection = mongo_client.get_collection("users")
        return users_collection.find_one({"googleID": id})

    def save_a_pet(self, pet: dict):
        try:
            new_pet = self.pets_collection.insert_one(pet)
            return new_pet.inserted_id
        except Exception as e:
            logging.error(f"An error occurred while saving the pet: {e}")
            return None

    def get_a_pet(self, pet_id: str) -> Union[dict, None]:
        pet_id = self.check_pet_id(pet_id)
        filter_criteria = {"_id": pet_id}
        pet = self.pets_collection.find_one(filter_criteria)
        self.serialize_a_complex_data(pet)
        return pet

    def get_pets_by_filters(self, *, filters: List) -> Union[List[any], None]:
        pets = list(self.pets_collection.find(filters))

        for pet in pets:
            self.serialize_a_complex_data(pet)

        return pets

    def serialize_a_complex_data(self, data):
        if data:
            data["_id"] = str(data["_id"])
            data["person"] = str(data["person"])

    def check_pet_id(self, id: str):
        if not isinstance(id, ObjectId):
            return ObjectId(id)
        return id

    def mofify_a_pet(self, new_data: dict, id: str) -> Tuple[int]:
        pet_id = self.check_pet_id(id)
        filter_criteria = {"_id": pet_id}
        new_data = {"$set": new_data}
        pet = self.pets_collection.update_one(filter_criteria, new_data)
        return pet.modified_count, pet.matched_count

    def delete_a_pet(self, id: str) -> None:
        pet_id = self.check_pet_id(id)
        filter_criteria = {"_id": pet_id}
        pet = self.pets_collection.delete_one(filter_criteria)
        self.serialize_a_complex_data(pet)
        return pet

    def create_a_pet(
        self, pet: dict, user_id: str, is_graphql_request: bool = False
    ) -> str:
        user = self.get_a_user_by_google_id(user_id)
        user = user["_id"]
        pet.update({"person": user})
        new_pet = self.pets_collection.insert_one(pet)
        if is_graphql_request:
            new_pet = self.get_a_pet(str(new_pet.inserted_id))
            new_pet["id"] = new_pet["_id"]
            del new_pet["_id"]
            return new_pet
        return str(new_pet.inserted_id)
