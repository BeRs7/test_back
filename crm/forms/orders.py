from django.forms import inlineformset_factory

from catalog.models import Product
from orders.models import Order, ProductInOrder
from utils.forms import StyledModelForm


class OrderUpdateForm(StyledModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class ProductInOrderForm(StyledModelForm):
    class Meta:
        model = ProductInOrder
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.prefetch_related("translations")


OrderProductsFormset = inlineformset_factory(
    model=ProductInOrder, form=ProductInOrderForm, parent_model=Order, extra=0, can_delete=True
)
