from django.urls import path
from .views import RequestAdoptionView

urlpatterns = [path("request/", RequestAdoptionView.as_view(), name="request_adoption")]
