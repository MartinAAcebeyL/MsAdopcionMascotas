from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.users.serialiezers import SubmitUserInfoSerializer


class SubmitUserInfo(APIView):
    serializer_class = SubmitUserInfoSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.update(request.user, serializer.validated_data)
            user["id"] = str(user.pop("_id"))
            return Response(user, status=201)
        except Exception as e:
            return Response({"error": e}, status=400)
