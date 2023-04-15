from pathlib import Path

from django.core.validators import MinValueValidator
from django.db import models


def get_upload_path(instance, filename, file_extension):
    return Path(f"products/{instance.id}/files/{filename}.{file_extension}")


class FileAbstractModel(models.Model):
    file = models.FileField(verbose_name="Файл", upload_to=get_upload_path)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    size = models.BigIntegerField(
        verbose_name="Размер файла в байтах",
        default=0,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.filename}"

    @property
    def full_filename(self):
        return f"{self.filename}.{self.file_extension}"

    @property
    def filename(self) -> str:
        """
        Название файла
        """
        return Path(self.file.name).name

    @property
    def file_extension(self):
        """
        Расширение файла
        """
        return Path(self.file.name).suffix

    @property
    def size_mb(self):
        return round(self.size * 0.000001, 3)

    @property
    def size_kb(self):
        return round(self.size * 0.001, 3)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.size:
            self.size = self.file.size
        super().save(force_insert, force_update, using, update_fields)
