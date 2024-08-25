from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .db import Adoption
from .serializers import AdoptionRequestSerializer, ListRequestAdoptionsSerializer
from utils import roles_required


class RequestAdoptionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdoptionRequestSerializer

    @roles_required(["adoptante"])
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


class ListRequestAdoptions(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListRequestAdoptionsSerializer

    @roles_required(["cliente"])
    def get(self, request):
        try:
            owner_id = request.user.id
            queryset = self.get_queryset(owner_id)

            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "error": e.detail if hasattr(e, "detail") else str(e),
                    "message": "An error occurred while listing the adoption requests.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_queryset(self, *args, **kwargs):
        adoption_model = Adoption()
        return adoption_model.get_adoption_requests(args[0])
