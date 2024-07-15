import graphene
import logging
from graphene import relay, Mutation
from graphene_django.types import DjangoObjectType
from django.core.exceptions import PermissionDenied

from .enum import SexEnum, SizeEnum, StatusEnum
from apps.pets.db.entity import PetEntity
from apps.pets.db.models import Pet
from apps.pets.serializers import CreatePet
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
class CreatePetMutation(Mutation):
    class Arguments:
        name = graphene.String()
        history = graphene.String()
        age_value = graphene.Int()
        age_time = graphene.String()
        breed = graphene.String()
        type = graphene.String()
        city = graphene.String()
        size = SizeEnum()
        sex = SexEnum()
        status = StatusEnum()

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
