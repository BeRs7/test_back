from rest_framework.serializers import ImageField
from sorl.thumbnail import get_thumbnail


class CropImageFieldSerializer(ImageField):
    read_only = True

    def __init__(self, geometry_string, options=None, context=None, *args, **kwargs):
        if context is None:
            context = {}
        if options is None:
            # без этих опций не кропает изображение под нужный размер
            options = {'crop': 'center', 'quality': 100}

        self.geometry_string = geometry_string
        self.options = options
        self._context = context
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        """
        Принимает аргументы фото, отдаёт юрл
        """

        if not value:
            return None

        file = self.crop_if_image(value)
        if file == '':
            return ''

        request = self.context.get("request", None)
        if request:
            return request.build_absolute_uri(file)
        else:
            return super().to_representation(file)

    def crop_if_image(self, file):
        if file.name.endswith('.png') or file.name.endswith('.jpeg') or file.name.endswith('.jpg'):
            file = get_thumbnail(file, self.geometry_string, **self.options)
            return file.url
        else:
            if 'get_file' in self.source_attrs:  # костыль
                return ''
            return f'/media/{file}'