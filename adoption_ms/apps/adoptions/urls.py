from django.urls import path
from .views import RequestAdoptionView, ListRequestAdoptions

urlpatterns = [
    path("request/", RequestAdoptionView.as_view(), name="request_adoption"),
    path("list", ListRequestAdoptions.as_view(), name="list_adoption_requests"),
]
