from graphene import ObjectType, String, Field
from graphene.relay import ConnectionField

from .types import PetType, PetConnection, FilterInputType
from apps.pets.db.models import Pet
from apps.pets.db.entity import PetEntity
from apps.pets.serializers import QueryParamsToFilterPets
from graphene import Argument


class Query(ObjectType):
    pet = Field(PetType, id=String())
    pets = ConnectionField(
        PetConnection, filter=Argument(FilterInputType, required=False)
    )

    def resolve_pet(self, _, id: str):
        pet_model = Pet()
        pet_data = pet_model.get_a_pet(id)

        if pet_data:
            pet_data["id"] = pet_data["_id"]
            del pet_data["_id"]
            return PetEntity(**pet_data)
        return None

    def resolve_pets(self, _, filter=None, **kwargs):
        def add_age_filter(data: dict) -> dict:

            if data.get("age_value") is not None and data.get("age_time") == "años":
                data["$or"] = [
                    {"age_time": "meses"},
                    {"age_time": "años", "age_value": {"$lte": data.get("age_value")}},
                ]
                data.pop("age_value", None)
                data.pop("age_time", None)
            if data.get("age_value") is not None and data.get("age_time") == "meses":
                data["age_value"] = {"$lte": data.get("age_value")}
                data["age_time"] = data.get("age_time")

        filters = filter or {}
        serializer = QueryParamsToFilterPets(data=filters)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data
        add_age_filter(filters)

        pet_model = Pet()
        pets = pet_model.get_pets_by_filters(filters=filters)
        array_pets = []
        for pet in pets:
            pet["id"] = pet["_id"]
            del pet["_id"]
            array_pets.append(PetEntity(**pet))
        return array_pets
