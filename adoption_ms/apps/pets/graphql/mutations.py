from graphene import ObjectType
from .types import CreatePetMutation


class Mutation(ObjectType):
    create_pet = CreatePetMutation.Field()
