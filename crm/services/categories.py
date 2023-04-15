from typing import List
from uuid import uuid4

from catalog.models import Category


class CategoryHelper:
    """
    Group actions on categories list
    """

    def disable_categories(self, ids: List[int]):
        return Category.objects.filter(id__in=ids).update(is_active=False)

    def enable_categories(self, ids: List[int]):
        return Category.objects.filter(id__in=ids).update(is_active=True)

    def delete_categories(self, ids: List[int]):
        return Category.objects.filter(id__in=ids).delete()

    def copy_categories(self, ids: List[int]):
        for category in Category.objects.filter(id__in=ids):
            translations = category.translations.all()
            category.id = None
            category.uid = uuid4()
            category.is_active = False
            category.slug = "{}-{}".format(category.slug, uuid4())
            category.save()
            for translation in translations:
                translation.pk = None
                translation.master = category
                translation.save()
