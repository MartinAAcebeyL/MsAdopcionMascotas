from django.urls import path

from .views import GetPetView, FilterPetView, PaginatePetView

urlpatterns = [
    path("get/<str:pk>", GetPetView.as_view(), name="get one pet"),
    path("filter", FilterPetView.as_view(), name="filter pets by criteria"),
    path("all", PaginatePetView.as_view(), name="Pagination of  all pets"),
]
