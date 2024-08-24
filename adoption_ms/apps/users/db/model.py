from bson import ObjectId

from frameworks import mongo_client


class UserModel:
    def __init__(self) -> None:
        self.users_collection = mongo_client.get_collection("users")

    def update_user(
        self, user_id: str, user_data: dict, is_complete_info: bool = False
    ) -> dict:
        if is_complete_info:
            user_data["is_complete_info"] = True

        user = self.users_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": user_data},
            return_document=True,
            projection={
                "password": False,
                "__v": False,
                "createdAt": False,
                "updatedAt": False,
                "deletedAt": False,
            },
        )
        return user
