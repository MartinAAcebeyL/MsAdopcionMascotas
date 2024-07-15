from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

from .views import GetUpdatePetView, FilterPetView, PaginatePetView, CreatePet
from .graphql import schema

urlpatterns = [
    path("<str:pk>", GetUpdatePetView.as_view(), name="get and update pet"),
    path("filter/criteria", FilterPetView.as_view(), name="filter pets by criteria"),
    path("get/all", PaginatePetView.as_view(), name="Pagination of all pets"),
    path("create/", CreatePet.as_view(), name="create-pet"),
    path(
        "graphql/",
        csrf_exempt(GraphQLView.as_view(schema=schema)),
        name="graphql",
    ),
]
