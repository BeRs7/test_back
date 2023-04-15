from rest_framework import serializers

from orders.models import RegistrationForFitting


class FittingRegistrationSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(input_formats=["iso-8601"])
    email = serializers.EmailField()

    class Meta:
        model = RegistrationForFitting
        fields = (
            "full_name",
            "phone",
            "email",
            "date_of_wedding",
            "comment",
            "time",
            "service_type",
        )
