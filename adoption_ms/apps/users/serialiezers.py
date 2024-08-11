from rest_framework import serializers

from .models import UserAuxiliar


class SubmitUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuxiliar
        fields = [
            "name",
            "last_name",
            "phone",
            "email",
            "address",
            "city",
            "country",
            "birth_date",
            "identity_document",
        ]
