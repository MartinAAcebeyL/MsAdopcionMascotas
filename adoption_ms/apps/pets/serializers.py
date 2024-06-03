from rest_framework import serializers


class BasePetAttributes(serializers.Serializer):
    value = serializers.IntegerField(min_value=0, required=False)
    unit = serializers.ChoiceField(choices=["años", "meses"], required=False)
    breed = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    history = serializers.CharField(required=False)
    sex = serializers.ChoiceField(choices=["F", "M"], required=False)
    size = serializers.ChoiceField(choices=["small", "middle", "big"], required=False)
    status = serializers.ChoiceField(
        choices=["progress", "adopted", "able"], required=False
    )


class QueryParamsToFilterPets(BasePetAttributes):
    def validate(self, data):
        validated_data = super().validate(data)

        if "value" in validated_data and "unit" not in validated_data:
            raise serializers.ValidationError(
                "El campo 'unit' es obligatorio cuando se proporciona el campo 'value'."
            )
        elif "unit" in validated_data and "value" not in validated_data:
            raise serializers.ValidationError(
                "El campo 'value' es obligatorio cuando se proporciona el campo 'unit'."
            )

        return validated_data


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
