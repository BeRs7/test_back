from typing import List

from orders.models import Order

# from orders.tasks import run_create_order_retail_crm_workload


class OrderHelper:
    """
    Group actions on orders list
    """

    def delete_orders(self, ids: List[int]):
        return Order.objects.filter(id__in=ids).delete()

    def copy_orders(self, ids: List[int]):
        for order in Order.objects.filter(id__in=ids):
            products_in_order = order.products.all()
            order.id = None
            order.save()
            for product_in_order in products_in_order:
                product_in_order.pk = None
                product_in_order.order = order
                product_in_order.save()

    # def send_orders_to_retail(self, ids):
    #     for order in Order.objects.filter(id__in=ids).exclude(country_iso=None):
    #         delivery_data = {
    #             "index": order.index,
    #             "street": order.street,
    #             "city": order.city,
    #             "house": order.house,
    #             "appartment": order.appartment,
    #             "country_iso": order.country_iso,
    #         }
    #         # run_create_order_retail_crm_workload.delay(order.id, delivery_data)
