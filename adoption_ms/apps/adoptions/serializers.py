import datetime
from bson import ObjectId
from rest_framework import serializers

from .db import Adoption, AdoptionEntity
from apps.pets.db.models import Pet
from apps.users.db import user_model


class BaseAdoptionAttributes(serializers.ModelSerializer):
    class Meta:
        model = AdoptionEntity
        fields = ["pet_id"]


class AdoptionRequestSerializer(BaseAdoptionAttributes):
    def save(self, **kwargs):
        adoption = Adoption()
        if not user_model.is_user_complete_info(kwargs["user_id"]):
            raise serializers.ValidationError(
                "The user has not completed their information."
            )
        if adoption.check_if_person_has_three_adoptions(kwargs["user_id"]):
            raise serializers.ValidationError("The user already has three adoptions.")

        if adoption.check_if_person_request_same_pet(
            kwargs["user_id"], ObjectId(self.validated_data["pet_id"])
        ):
            raise serializers.ValidationError("The user already requested this pet.")

        pet_model = Pet()
        pet = pet_model.get_a_pet(self.validated_data["pet_id"])
        print(pet)

        validated_data = {
            "pet_id": ObjectId(self.validated_data["pet_id"]),
            "user_id": kwargs["user_id"],
            "owner_id": ObjectId(pet["person"]),
            "status": "progress",
            "created_at": datetime.datetime.now(),
        }
        pet_model.mofify_a_pet({"status": "progress"}, validated_data["pet_id"])

        return adoption.save_an_adoption(validated_data)


class ListRequestAdoptionsSerializer(serializers.ModelSerializer):
    pet_info = serializers.SerializerMethodField()

    class Meta:
        model = AdoptionEntity
        fields = ["_id", "pet_info", "status", "created_at", "owner_id", "user_id"]

    def get_pet_info(self, obj):
        pet = obj["pet_info"]
        return {
            "name": pet["name"],
            "age": f"{pet['age_value']} {pet['age_time']}",
            "breed": pet["breed"],
            "type": pet["type"],
            "size": pet["size"],
            "sex": pet["sex"],
        }
