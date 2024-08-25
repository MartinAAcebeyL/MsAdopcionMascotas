from django.urls import path
from .views import RequestAdoptionView, ListRequestAdoptions, AcceptOrRejectAdoptionView

urlpatterns = [
    path("request/", RequestAdoptionView.as_view(), name="request_adoption"),
    path("list", ListRequestAdoptions.as_view(), name="list_adoption_requests"),
    path(
        "<slug:action>/<str:adoption_id>",
        AcceptOrRejectAdoptionView.as_view(),
        name="accept_reject_adoption",
    ),
]
