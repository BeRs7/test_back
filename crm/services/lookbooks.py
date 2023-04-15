from typing import List
from uuid import uuid4

from lookbook.models import LookBook


class LookBookHelper:
    """
    Group actions on products list
    """

    def disable_lookbooks(self, ids: List[int]):
        return LookBook.objects.filter(id__in=ids).update(is_published=False)

    def enable_lookbooks(self, ids: List[int]):
        return LookBook.objects.filter(id__in=ids).update(is_published=True)

    def delete_lookbooks(self, ids: List[int]):
        return LookBook.objects.filter(id__in=ids).delete()

    def copy_lookbooks(self, ids: List[int]):
        for lookbook in LookBook.objects.filter(id__in=ids):
            translations = lookbook.translations.all()
            lookbook.id = None
            lookbook.slug = "{}-{}".format(lookbook.slug, uuid4())
            lookbook.save()
            for translation in translations:
                translation.pk = None
                translation.master = lookbook
                translation.save()
