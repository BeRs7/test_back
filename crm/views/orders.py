# from django.shortcuts import redirect
from django.urls import reverse

# from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView
from django_filters.views import FilterView

from crm.filters.custom_filter import CustomFilter
from crm.filters.orders import CRMOrdersFilter

# from crm.services.orders import OrderHelper
from orders.models import Order
from utils.decorators import crm_member_required


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMOrderListView(FilterView, CustomFilter):
    template_name = "crm/orders/orders.html"
    paginate_by = 50
    context_object_name = "orders"
    filterset_class = CRMOrdersFilter

    def get_queryset(self):
        return Order.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        checkboxes_list = ["new", "canceled", "payed"]
        context.update(
            {
                "delete_orders_url": reverse("crm:api:orders:delete-orders"),
                "copy_orders_url": reverse("crm:api:orders:copy-orders"),
                # "send_to_retail_url": reverse("crm:api:orders:send-to-retail-orders"),
                "has_filter_status": self._get_has_filter_from_checkboxes(
                    filters_data=self.filterset.data, args=checkboxes_list
                ),
                "has_filter_date": True
                if (self.filterset.data.get("date_start", None) or self.filterset.data.get("date_end", None))
                else False,
            }
        )
        return context


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMOrderUpdateView(DetailView):
    template_name = "crm/orders/order.html"
    context_object_name = "order"
    queryset = Order.objects.prefetch_related("order_products", "order_products__product__translations")


# @method_decorator(crm_member_required, "dispatch")
# class CRMOrderSendToRetailView(DetailView):
#     queryset = Order.objects.prefetch_related("order_products", "order_products__product__translations")
#
#     def get(self, request, *args, **kwargs):
#         order = self.get_object()
#         OrderHelper().send_orders_to_retail((order.id,))
#         messages.success(self.request, "Заказ отправлен в RetailCRM и появится там в ближайшее время")
#         return redirect(request.META.get("HTTP_REFERER"))
