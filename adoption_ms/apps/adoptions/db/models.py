import logging

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
