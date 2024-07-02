from django.urls import path

from .views import GetUpdatePetView, FilterPetView, PaginatePetView, CreatePet

urlpatterns = [
    path("<str:pk>", GetUpdatePetView.as_view(), name="get and update pet"),
    path("filter", FilterPetView.as_view(), name="filter pets by criteria"),
    path("all", PaginatePetView.as_view(), name="Pagination of all pets"),
    path("create/", CreatePet.as_view(), name="create-pet"),
]
