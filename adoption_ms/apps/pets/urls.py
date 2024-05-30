from django.urls import path

from .views import GetPetView, FilterPetView

urlpatterns = [
    path("get/<str:pk>", GetPetView.as_view(), name="get one pet"),
    path("filter", FilterPetView.as_view(), name="filter pets by criteria"),
]
