import requests
from rest_framework import authentication, exceptions
from django.contrib.auth.models import User

from apps.pets.models import Pet


class GoogleOAuth2Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return None
        token = parts[1]

        user_info = self.__verify_google_token(token)
        if user_info is None:
            raise exceptions.AuthenticationFailed("Invalid token.")

        user = self.__get_user(user_info)
        return user, None

    def __verify_google_token(self, token):
        response = requests.get(
            f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}"
        )
        if response.status_code != 200:
            return None
        return response.json()

    def __get_user(self, user_info):
        user = Pet.get_a_user_by_google_id(user_info.get("user_id"))
        return self.__create_django_user(user)

    def __create_django_user(self, user_data):
        user = User(
            id=user_data["_id"],
            username=user_data["googleID"],
            email=user_data["email"],
            first_name=user_data["name"],
            last_name=user_data["lastName"],
        )
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.set_unusable_password()
        return user
