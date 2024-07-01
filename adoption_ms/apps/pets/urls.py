from django.urls import path

from .views import GetUpdateCreatePetView, FilterPetView, PaginatePetView

urlpatterns = [
    path(
        "<str:pk>",
        GetUpdateCreatePetView.as_view(),
        name="get, update and create pet",
    ),
    path("filter", FilterPetView.as_view(), name="filter pets by criteria"),
    path("all", PaginatePetView.as_view(), name="Pagination of  all pets"),
]
