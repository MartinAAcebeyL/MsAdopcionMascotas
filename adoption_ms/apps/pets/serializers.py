from rest_framework import serializers


class BasePetAttributes(serializers.Serializer):
    value = serializers.IntegerField(min_value=0, required=False)
    unit = serializers.ChoiceField(choices=["años", "meses"], required=False)
    breed = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=["gato", "perro"], required=False)
    history = serializers.CharField(required=False)
    sex = serializers.ChoiceField(choices=["F", "M"], required=False)
    size = serializers.ChoiceField(choices=["small", "middle", "big"], required=False)
    status = serializers.ChoiceField(
        choices=["progress", "adopted", "able"], required=False
    )
    breed = serializers.CharField(required=False)


class QueryParamsToFilterPets(BasePetAttributes):
    def validate(self, data):
        validated_data = super().validate(data)
        self.validate_mutual_dependence(validated_data, "value", "unit")
        self.validate_dependence(
            data=validated_data, dependencie_a="breed", dependencie_b="type"
        )

        return validated_data

    def validate_mutual_dependence(self, data, dependencie_a: str, dependencie_b: str):
        if dependencie_a in data and dependencie_b not in data:
            raise serializers.ValidationError(
                f"El campo {dependencie_b} es obligatorio cuando se proporciona el campo {dependencie_a}."
            )
        elif dependencie_b in data and dependencie_a not in data:
            raise serializers.ValidationError(
                f"El campo {dependencie_a} es obligatorio cuando se proporciona el campo {dependencie_b}."
            )

    def validate_dependence(self, *, data, dependencie_a: str, dependencie_b: str):
        if dependencie_a in data and dependencie_b not in data:
            raise serializers.ValidationError(
                f"El campo {dependencie_b} es obligatorio cuando se proporciona el campo {dependencie_a}."
            )


class GetUpdatePet(QueryParamsToFilterPets):
    """
    Get and updates pet data with validation based on QueryParamsToFilterPets class.
    """


class CreatePet(QueryParamsToFilterPets):
    """
    Create pet data with validation based on QueryParamsToFilterPets class.
    """


class PetRepresentation(BasePetAttributes):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        age = instance.get("age", [1, "mes"])

        return {
            "edad": f"{age[0]} {age[1]}",
            "raza": rep.get("breed", ""),
            "ciudad": rep.get("city", ""),
            "sexo": "Macho" if rep.get("sex") == "M" else "Hembra",
            "tamaño": rep.get("size", ""),
            "estado": rep.get("status", ""),
            "nombre": rep.get("name", ""),
            "history": rep.get("history", ""),
        }
