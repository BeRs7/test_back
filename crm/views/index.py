from datetime import timedelta

from django.db.models import Count, Avg
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache

from orders.models import Order
from utils.decorators import crm_member_required


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMIndexView(generic.TemplateView):
    template_name = "crm/utils/crm_index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        last_30_days = timezone.now() - timedelta(days=30)
        previous_30_days = timezone.now() - timedelta(days=60)
        orders_current_month = Order.objects.filter(created_at__gt=last_30_days)
        orders_previous_month = Order.objects.filter(created_at__gt=previous_30_days, created_at__lt=last_30_days)
        products_current_month_quantity = orders_current_month.aggregate(Count("order_products")).get(
            "order_products__count"
        )
        products_previous_month_quantity = orders_previous_month.aggregate(Count("order_products")).get(
            "order_products__count"
        )
        avg_current_month_receipt_amount = int(
            orders_current_month.aggregate(Avg("summary_cost")).get("summary_cost__avg") or 1
        )
        avg_previous_month_receipt_amount = int(
            orders_previous_month.aggregate(Avg("summary_cost")).get("summary_cost__avg") or 1
        )
        context.update(
            {
                "orders_count": orders_current_month.count(),
                "orders_percent": orders_current_month.count() // (orders_previous_month.count() or 1)
                if orders_current_month.count() > orders_previous_month.count()
                else -orders_previous_month.count() // (orders_current_month.count() or 1),
                "products_quantity": products_current_month_quantity,
                "products_percent": products_current_month_quantity // (products_previous_month_quantity or 1)
                if products_current_month_quantity > products_previous_month_quantity
                else -products_previous_month_quantity // (products_current_month_quantity or 1),
                "avg_receipt": avg_current_month_receipt_amount,
                "avg_receipt_percent": int(
                    (avg_current_month_receipt_amount / avg_previous_month_receipt_amount) * 100
                )
                if avg_current_month_receipt_amount > avg_previous_month_receipt_amount
                else -int((avg_previous_month_receipt_amount / avg_current_month_receipt_amount) * 100),
            }
        )
        return context
