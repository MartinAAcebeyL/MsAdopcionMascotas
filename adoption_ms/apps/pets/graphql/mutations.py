from graphene import ObjectType
from .types import CreatePetMutation, UpdatePetMutation


class Mutation(ObjectType):
    create_pet = CreatePetMutation.Field()
    update_pet = UpdatePetMutation.Field()
