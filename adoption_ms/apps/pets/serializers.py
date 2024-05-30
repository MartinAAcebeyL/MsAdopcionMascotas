from rest_framework import serializers


class QueryParamsToFilterPets(serializers.Serializer):
    value = serializers.IntegerField(min_value=0, required=False)
    unit = serializers.ChoiceField(choices=["años", "meses"], required=False)
    breed = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    sex = serializers.ChoiceField(choices=["F", "M"], required=False)
    size = serializers.ChoiceField(choices=["small", "middle", "big"], required=False)
    status = serializers.ChoiceField(
        choices=["progress", "adopted", "able"], required=False
    )

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
