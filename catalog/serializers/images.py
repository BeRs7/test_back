from rest_framework import serializers

from catalog.models import ProductGallery
from utils.files.serializers import CropImageFieldSerializer


class ImageSerializer(serializers.ModelSerializer):
    """
    Кроп фото для отображения в списке товаров/деталях товара
    """

    large_file = CropImageFieldSerializer("1800x2656", options={"crop": "center"}, source="get_file")
    file = CropImageFieldSerializer("1179x1740", options={"crop": "center"})
    type = serializers.SerializerMethodField()

    class Meta:
        model = ProductGallery
        fields = ["file", "large_file", "type"]

    def get_type(self, instance):
        file_name = instance.file.name
        if file_name.endswith('.png') or file_name.endswith('.jpeg') or file_name.endswith('.jpg'):
            return "image"
        else:
            return "video"
