from django.http import JsonResponse, HttpResponse
from django.views import generic

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from utils.forms import TempFileForm
from utils.serializers.temp_file import TempFileSerializer


class AjaxUploadTempFile(generic.View):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = TempFileForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                instance = form.save()
                data = {"is_error": False, "file_id": instance.pk, "file_url": instance.file.url}
            else:
                data = {"is_error": True}
            return JsonResponse(data)
        else:
            return HttpResponse(status=404)


class TempFileUploader(CreateAPIView):
    serializer_class = TempFileSerializer
    permission_classes = [AllowAny]
