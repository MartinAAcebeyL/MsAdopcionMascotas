import datetime
from bson import ObjectId
from rest_framework import serializers

from .db import Adoption, AdoptionEntity
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

        validated_data = {
            "pet_id": ObjectId(self.validated_data["pet_id"]),
            "user_id": kwargs["user_id"],
            "status": "progress",
            "created_at": datetime.datetime.now(),
        }

        return adoption.save_an_adoption(validated_data)
