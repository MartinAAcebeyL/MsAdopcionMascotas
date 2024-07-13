from graphene import ObjectType, String, Field
from .types import PetType
from apps.pets.db.models import Pet
from apps.pets.db.entity import PetEntity


class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))
    pet = Field(PetType, id=String())

    def resolve_hello(self, _, name):
        return f"Hello {name}!"

    def resolve_pet(self, _, id: str):
        pet_model = Pet()
        pet_data = pet_model.get_a_pet(id)

        if pet_data:
            pet_data["mongo_id"] = pet_data["_id"]
            del pet_data["_id"]
            return PetEntity(**pet_data)
        return None
