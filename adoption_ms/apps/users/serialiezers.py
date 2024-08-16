from rest_framework import serializers

from .db.entity import UserAuxiliar
from .db.model import UserModel


class SubmitUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuxiliar
        fields = [
            "phone",
            "address",
            "city",
            "country",
            "birth_date",
            "identity_document",
        ]

    def update(self, instance, validated_data):
        user_model = UserModel()
        return user_model.update_user(
            str(instance.id), validated_data, is_complete_info=True
        )
