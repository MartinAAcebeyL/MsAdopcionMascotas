from typing import List
from functools import wraps
from rest_framework import status
from rest_framework.response import Response

from frameworks import mongo_client


def roles_required(roles: List[str]):
    def decorator(func):
        @wraps(func)
        def wrapper_view(view, *args, **kwargs):
            request = view.request
            user_id = request.user.id

            user_collection = mongo_client.get_collection("users")
            user = user_collection.find_one({"_id": user_id})
            
            user_roles = user["roles"]
            roles_collection = mongo_client.get_collection("roles")
            user_roles = list(
                roles_collection.find(
                    {"_id": {"$in": user_roles}},
                    projection={"description": False, "_id": False},
                )
            )
            user_roles = [role["name"] for role in user_roles]


            if user and any(role in user_roles for role in roles):
                return func(view, *args, **kwargs)
            return Response(
                {
                    "message": "You do not have permission to access this resource.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        return wrapper_view

    return decorator
