from django.urls import path

from .views import GetPetView

urlpatterns = [
    path("get/<str:pk>", GetPetView.as_view(), name="get one pet"),
]
