import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from bson import ObjectId

from .db import Adoption
from .serializers import AdoptionRequestSerializer, ListRequestAdoptionsSerializer
from apps.pets.db.models import Pet
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


class AcceptOrRejectAdoptionView(APIView):
    permission_classes = [IsAuthenticated]

    @roles_required(["cliente"])
    def put(self, request, action, adoption_id):
        try:
            adoption_model = Adoption()
            adoption_id = ObjectId(adoption_id)
            adoption = adoption_model.get_adoption_request_by_id(
                adoption_id, is_to_accept_or_reject=True
            )

            self.validations(adoption, action, request)

            adoption_model.accept_or_reject_adoption_request(
                adoption_id, action, request.data.get("comments", "")
            )
            Pet().mofify_a_pet(
                new_data={
                    "status": "adopted" if action == "accept" else "able",
                },
                id=adoption["pet_id"],
            )
            return Response(
                {"message": "Adoption request updated successfully."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            personal_data = e.args[0] if hasattr(e, "args") else {}

            error = personal_data.get("message", e)
            status_code = personal_data.get("status", 400)

            return Response(
                {
                    "error": error,
                    "message": "An error occurred while updating the adoption request.",
                },
                status=status_code,
            )

    def validations(self, adoption: Adoption, action: str, request):

        if not adoption:
            raise Exception({"message": "Adoption request not found.", "status": 404})

        if adoption["owner_id"] != request.user.id:
            raise Exception(
                {
                    "message": "You do not have permission to perform this action.",
                    "status": 403,
                }
            )

        if action == "reject" and not request.data.get("comments"):
            raise Exception(
                {
                    "message": "Comments are required to reject the adoption request.",
                    "status": 400,
                }
            )
