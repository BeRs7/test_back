from typing import List
from uuid import uuid4

from catalog.models import Product


class ProductHelper:
    """
    Group actions on products list
    """

    def disable_products(self, ids: List[int]):
        return Product.objects.filter(id__in=ids).update(is_active=False)

    def enable_products(self, ids: List[int]):
        return Product.objects.filter(id__in=ids).update(is_active=True)

    def delete_products(self, ids: List[int]):
        return Product.objects.filter(id__in=ids).delete()

    def copy_products(self, ids: List[int]):
        for product in Product.objects.filter(id__in=ids):
            images = product.images.all()
            materials = product.materials.all()
            storages = product.storages.all()
            translations = product.translations.all()
            product.set_current_language("ru")
            product.id = None
            product.uid = None
            product.external_id = None
            product.sku = None
            product.slug = "{}-{}".format(product.slug, uuid4())
            product.is_active = False
            product.save()
            for image in images:
                image.pk = None
                image.product = product
                image.save()
            for material in materials:
                material.pk = None
                material.product = product
                material.save()
            for storage in storages:
                storage.pk = None
                storage.product = product
                storage.save()
            for translation in translations:
                translation.pk = None
                translation.master = product
                translation.save()
