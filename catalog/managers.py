from django.db.models import Q
from mptt.managers import TreeManager
from mptt.querysets import TreeQuerySet
from parler.managers import TranslatableQuerySet, TranslatableManager


class CategoryQuerySet(TranslatableQuerySet, TreeQuerySet):
    def as_manager(cls):
        manager = CategoryManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)


class CategoryManager(TreeManager, TranslatableManager):
    _queryset_class = CategoryQuerySet

    def active(self):
        return self.filter(is_active=True).prefetch_related("translations", "parent")

    def main(self):
        return self.filter(Q(is_active=True, on_main=True) & ~Q(Q(cover="") | Q(cover=None))).prefetch_related(
            "translations", "parent"
        )

    def on_transactions(self):
        return self.filter(Q(is_active=True, on_transactions=True) & ~Q(Q(cover="") | Q(cover=None))).prefetch_related(
            "translations", "parent"
        )
