from rest_framework.views import APIView
from rest_framework.response import Response


class SubmitUserInfo(APIView):
    def post(self, request):
        return Response({"message": "User information submitted."})
