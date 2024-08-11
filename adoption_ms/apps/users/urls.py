from django.urls import path

from .views import SubmitUserInfo


urlpatterns = [
    path(
        "submit-information/", SubmitUserInfo.as_view(), name="submit_user_information"
    ),
]
