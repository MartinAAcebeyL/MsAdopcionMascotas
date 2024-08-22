import logging
from typing import Union, List
from bson import ObjectId

from frameworks import mongo_client


class Adoption:
    def __init__(self) -> None:
        self.collection = mongo_client.get_collection("adoptions")

    def save_an_adoption(self, adoption: dict):
        try:
            new_adoption = self.collection.insert_one(adoption)
            return new_adoption.inserted_id
        except Exception as e:
            logging.error(f"An error occurred while saving the adoption: {e}")
            return None

    def check_if_person_request_same_pet(self, person_id: str, pet_id: str) -> bool:
        filter_criteria = {"user_id": person_id, "pet_id": pet_id}
        adoption = self.collection.find_one(filter_criteria)
        return adoption is not None

    def check_if_person_has_three_adoptions(self, person_id: str) -> bool:
        filter_criteria = {"user_id": person_id}
        adoptions = list(self.collection.find(filter_criteria))
        return len(adoptions) >= 3

    def get_an_adoption(self, adoption_id: str) -> Union[dict, None]:
        adoption_id = self.check_adoption_id(adoption_id)
        filter_criteria = {"_id": adoption_id}
        adoption = self.collection.find_one(filter_criteria)
        self.serialize_a_complex_data(adoption)
        return adoption

    def get_adoptions_by_filters(self, *, filters: List) -> Union[List[any], None]:
        adoptions = list(self.collection.find(filters))

        for adoption in adoptions:
            self.serialize_a_complex_data(adoption)

        return adoptions

    def serialize_a_complex_data(self, data):
        if data:
            data["_id"] = str(data["_id"])
            data["person"] = str(data["person"])
            data["pet"] = str(data["pet"])
            data["adoption_date"] = str(data["adoption_date"])

    def check_adoption_id(self, id: str):
        if not isinstance(id, ObjectId):
            return ObjectId(id)
        return id
