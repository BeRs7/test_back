from django.db import models


class TempFile(models.Model):
    file = models.FileField(upload_to="tmp/")
