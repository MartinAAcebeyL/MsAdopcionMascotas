import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import AdoptionRequestSerializer


class RequestAdoptionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdoptionRequestSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id=request.user.id)
            return Response(
                {"message": "Adoption request created successfully."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    "error": e.detail if hasattr(e, "detail") else str(e),
                    "message": "An error occurred while creating the adoption request.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
