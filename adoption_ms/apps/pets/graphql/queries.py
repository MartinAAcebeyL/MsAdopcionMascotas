from graphene import ObjectType, String, Field
from graphene.relay import ConnectionField

from .types import PetType, PetConnection
from apps.pets.db.models import Pet
from apps.pets.db.entity import PetEntity


class Query(ObjectType):
    pet = Field(PetType, id=String())
    pets = ConnectionField(PetConnection)

    def resolve_pet(self, _, id: str):
        pet_model = Pet()
        pet_data = pet_model.get_a_pet(id)

        if pet_data:
            pet_data["id"] = pet_data["_id"]
            del pet_data["_id"]
            return PetEntity(**pet_data)
        return None

    def resolve_pets(self, _, **kwargs):
        pet_model = Pet()
        pets = pet_model.get_pets_by_filters(filters={})

        array_pets = []
        for pet in pets:
            pet["id"] = pet["_id"]
            del pet["_id"]
            array_pets.append(PetEntity(**pet))
        return array_pets
