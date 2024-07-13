from graphene_django.types import DjangoObjectType
from apps.pets.db.entity import PetEntity


class PetType(DjangoObjectType):
    class Meta:
        model = PetEntity
        fields = "__all__"
