from rest_framework import serializers

from utils.models.temp_file import TempFile


class TempFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TempFile
        fields = [
            "id",
            "file"
        ]
