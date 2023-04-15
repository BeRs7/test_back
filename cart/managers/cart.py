from django.db.models import QuerySet, Q

__all__ = ("CartQuerySet",)


class CartQuerySet(QuerySet):
    def active(self):
        return self.filter(~Q(status="payed")).prefetch_related(
            "products__trade_offer__product",
            "products__trade_offer__product__translations",
            "products__trade_offer__size",
            "products__trade_offer__size__translations",
            "products__trade_offer__product__color",
            "products__trade_offer__product__color__translations",
            "products__trade_offer__product__colors",
            "products__trade_offer__product__colors__translations",
            "products__trade_offer__product__colors__color",
            "products__trade_offer__product__colors__color__translations",
            "products__trade_offer__product__trade_offers",
            "products__trade_offer__product__trade_offers__size",
            "products__trade_offer__product__trade_offers__size__translations",
        )
