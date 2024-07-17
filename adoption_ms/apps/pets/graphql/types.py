import graphene
import logging
from graphene import relay, Mutation
from graphene_django.types import DjangoObjectType
from django.core.exceptions import PermissionDenied

from .enum import SexEnum, SizeEnum, StatusEnum
from apps.pets.db.entity import PetEntity
from apps.pets.db.models import Pet
from apps.pets.serializers import CreatePet, GetUpdatePet
from adoption_ms.authentication import GoogleOAuth2Authentication


class PetType(DjangoObjectType):
    class Meta:
        model = PetEntity
        fields = "__all__"


class PetNodeType(DjangoObjectType):
    class Meta:
        model = PetEntity
        interfaces = (relay.Node,)
        fields = "__all__"


class PetConnection(relay.Connection):
    class Meta:
        node = PetNodeType


# Mutations
class UpdateResponseType(graphene.ObjectType):
    message = graphene.String()
    id = graphene.ID(required=True)
    name = graphene.String()
    history = graphene.String()
    age_value = graphene.Int()
    age_time = graphene.String()
    breed = graphene.String()
    type = graphene.String()
    city = graphene.String()
    size = SizeEnum()
    status = StatusEnum()


class CreatePetMutation(Mutation):
    class Arguments:
        name = graphene.String(required=True)
        history = graphene.String()
        age_value = graphene.Int(required=True)
        age_time = graphene.String(required=True)
        breed = graphene.String()
        type = graphene.String()
        city = graphene.String(required=True)
        size = SizeEnum()
        sex = SexEnum()
        status = StatusEnum(default_value="available")

    pet = graphene.Field(PetType)

    @classmethod
    def mutate(cls, _, info, **kwargs):
        try:
            auth = GoogleOAuth2Authentication()
            user, _ = auth.authenticate(info.context)
            if not user:
                raise PermissionDenied("You must be logged to create a pet")
            serializer = CreatePet(data=kwargs)
            serializer.is_valid(raise_exception=True)
            pet_model = Pet()
            new_pet = pet_model.create_a_pet(
                serializer.validated_data, user.username, True
            )
            return CreatePetMutation(pet=PetEntity(**new_pet))
        except Exception as e:
            logging.error(f"An error occurred while creating a pet: {e}")
            raise e


class UpdatePetMutation(Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        history = graphene.String()
        age_value = graphene.Int()
        age_time = graphene.String()
        breed = graphene.String()
        type = graphene.String()
        city = graphene.String()
        size = SizeEnum()
        status = StatusEnum()

    pet = graphene.Field(UpdateResponseType)

    @classmethod
    def mutate(cls, _, info, **kwargs):
        try:

            auth = GoogleOAuth2Authentication()
            user, _ = auth.authenticate(info.context)
            if not user:
                raise PermissionDenied("You must be logged to update a pet")
            serializer = GetUpdatePet(data=kwargs)
            serializer.is_valid(raise_exception=True)

            pet_model = Pet()
            pet_id = kwargs.get("id")
            modified_count, matched_count = pet_model.mofify_a_pet(
                serializer.validated_data, pet_id
            )
            message = ""
            response = {
                "id": str(pet_id),
                **serializer.validated_data,
            }

            if modified_count == 0 and matched_count == 1:
                message = f"To pet with id {pet_id} the data you send is the same as the saved ones"
            elif matched_count == 0:
                message = f"pet with id {pet_id} was not found"
            elif modified_count == 1:
                message = f"pet with id {pet_id} was updated"

            response["message"] = message
            return UpdatePetMutation(pet=UpdateResponseType(**response))
        except Exception as e:
            logging.error(f"An error occurred while updating a pet: {e}")
            raise e
