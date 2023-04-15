from parler.managers import TranslatableQuerySet


class BannerQuerySet(TranslatableQuerySet):
    def banners_for_show(self):
        return self.filter(is_active=True).prefetch_related("translations")
