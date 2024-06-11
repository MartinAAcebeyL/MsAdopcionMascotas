from abc import ABC, abstractmethod
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status

from .models import Pet
from .serializers import (
    QueryParamsToFilterPets,
    PetRepresentation,
    UpdatePet,
)
from utils import CustomPagination

VALUE_POSITION = "age.0"
UNIT_POSITION = "age.1"


class CommonPetMethods(ABC):
    def _get_validated_data(self, *, validated_data):
        return {
            "sex": validated_data.get("sex"),
            "breed": validated_data.get("breed"),
            "city": validated_data.get("city"),
            "size": validated_data.get("size"),
            "status": validated_data.get("status"),
            "value": validated_data.get("value"),
            "unit": validated_data.get("unit"),
            "type": validated_data.get("unit"),
        }

    def _prepare_data(self, validated_data: dict) -> dict:
        data = {}
        if validated_data.get("sex"):
            data["sex"] = validated_data.get("sex")
        if validated_data.get("breed"):
            data["breed"] = validated_data.get("breed")
        if validated_data.get("city"):
            data["city"] = validated_data.get("city")
        if validated_data.get("size"):
            data["size"] = validated_data.get("size")
        if validated_data.get("status"):
            data["status"] = validated_data.get("status")
        if validated_data.get("type"):
            data["type"] = validated_data.get("type")
        self.modify_age_param(data, validated_data)
        return data

    @abstractmethod
    def modify_age_param(self, data: dict, base_data: dict) -> None:
        pass


class GetUpdateCreatePetView(APIView, CommonPetMethods):
    serializer_class = UpdatePet

    def get(self, request, pk):
        try:
            pet_model = Pet()
            pet = pet_model.get_a_pet(pk)
            if pet:
                return Response(pet, status=status.HTTP_200_OK)
            return Response(
                {"message": f"Pet with id {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk):
        try:
            body = request.data
            pet_model = Pet()
            pet_data = self.get_prepare_data_to_updated(body=body)
            modified_count, matched_count = pet_model.mofify_a_pet(pet_data, pk)

            if modified_count == 0 and matched_count == 1:
                return Response(
                    {
                        "message": f"To pet with id {pk} the data you send is the same as the saved ones"
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            elif matched_count == 0:
                return Response(
                    {"message": f"pet with id {pk} was not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            elif modified_count == 1:
                return Response(
                    {"message": f"pet with id {pk} was updated"},
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_prepare_data_to_updated(self, body: dict) -> dict:
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        validated_data_by_serializer = serializer.validated_data
        pet_data_validate = self._get_validated_data(
            validated_data=validated_data_by_serializer
        )
        return self._prepare_data(pet_data_validate)

    def modify_age_param(self, data, base_data):
        data[VALUE_POSITION] = base_data.get("value")
        data[UNIT_POSITION] = base_data.get("unit")


class FilterPetView(APIView, CommonPetMethods):
    serializer_class = QueryParamsToFilterPets

    def get(self, request):
        try:
            serializer = self.serializer_class(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            query_params = self._get_validated_data(validated_data=validated_data)
            filter_criteria = self._prepare_data(query_params)
            pet_model = Pet()
            pets = pet_model.get_pets_by_filters(filters=filter_criteria)
            return Response(pets, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def modify_age_param(self, data, base_data):
        data[VALUE_POSITION] = {"$lte": base_data.get("value")}
        data[UNIT_POSITION] = base_data.get("unit")
        return data


class PaginatePetView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = PetRepresentation

    def get_queryset(self):
        pet_model = Pet()
        queryset = pet_model.get_pets_by_filters(filters={})
        return queryset
