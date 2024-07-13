from graphene import relay
from graphene_django.types import DjangoObjectType
from apps.pets.db.entity import PetEntity


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
