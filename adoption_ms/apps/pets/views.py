from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Pet


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
