from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status

from .models import Pet
from .serializers import QueryParamsToFilterPets, PetRepresentation
from utils import CustomPagination, StandardResultsSetPagination


class GetPetView(APIView):
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


class FilterPetView(APIView):
    serializer_class = QueryParamsToFilterPets

    def get(self, request):
        try:
            serializer = self.serializer_class(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            query_params = self.__get_query_params(validated_data=validated_data)
            filter_criteria = self.__prepare_filters(query_params)
            pet_model = Pet()
            pets = pet_model.get_pets_by_filters(filters=filter_criteria)
            return Response(pets, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def __get_query_params(self, *, validated_data):
        return {
            "sex": validated_data.get("sex"),
            "breed": validated_data.get("breed"),
            "city": validated_data.get("city"),
            "size": validated_data.get("size"),
            "status": validated_data.get("status"),
            "value": validated_data.get("value"),
            "unit": validated_data.get("unit"),
        }

    def __prepare_filters(self, query_params):
        filter_criteria = {}
        if query_params.get("sex"):
            filter_criteria["sex"] = query_params.get("sex")
        if query_params.get("breed"):
            filter_criteria["breed"] = query_params.get("breed")
        if query_params.get("city"):
            filter_criteria["city"] = query_params.get("city")
        if query_params.get("size"):
            filter_criteria["size"] = query_params.get("size")
        if query_params.get("status"):
            filter_criteria["status"] = query_params.get("status")
        if query_params.get("value") and query_params.get("unit"):
            filter_criteria["age.0"] = {"$lte": query_params.get("value")}
            filter_criteria["age.1"] = query_params.get("unit")

        return filter_criteria


class PaginatePetView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = PetRepresentation

    def get_queryset(self):
        pet_model = Pet()
        queryset = pet_model.get_pets_by_filters(filters={})
        return queryset
