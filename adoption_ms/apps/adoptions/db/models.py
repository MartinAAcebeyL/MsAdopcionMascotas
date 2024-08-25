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

    def get_adoption_requests(self, owner_id: str):
        pipeline = [
            {
                "$match": {
                    "owner_id": owner_id,
                }
            },
            {
                "$lookup": {
                    "from": "pets",
                    "localField": "pet_id",
                    "foreignField": "_id",
                    "as": "pet_info",
                }
            },
            {"$unwind": "$pet_info"},
            {
                "$project": {
                    "_id": 1,
                    "user_id": 1,
                    "owner_id": 1,
                    "pet_info.name": 1,
                    "pet_info.age_value": 1,
                    "pet_info.age_time": 1,
                    "pet_info.breed": 1,
                    "pet_info.type": 1,
                    "pet_info.size": 1,
                    "pet_info.sex": 1,
                    "status": 1,
                    "created_at": 1,
                }
            },
        ]
        return list(self.collection.aggregate(pipeline))
