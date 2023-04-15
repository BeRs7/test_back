from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django_filters.views import FilterView

from catalog.models import Product
from crm.filters.custom_filter import CustomFilter
from crm.filters.products import CRMProductFilter
from crm.forms.product import ProductUpdateForm, ProductGalleryFormSet, ProductTradeOffersFormSet

from utils.decorators import crm_member_required


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMProductsListView(FilterView, CustomFilter):
    template_name = "crm/products/products.html"
    paginate_by = 50
    context_object_name = "products"
    filterset_class = CRMProductFilter
    allow_empty = True
    strict = False
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        checkboxes_list = ["is_active"]
        context.update(
            {
                "disable_products_url": reverse("crm:api:products:disable-products"),
                "enable_products_url": reverse("crm:api:products:enable-products"),
                "delete_products_url": reverse("crm:api:products:delete-products"),
                # "copy_products_url": reverse("crm:api:products:copy-products"),
                # filters
                "has_filter_status": self._get_has_filter_from_checkboxes(
                    filters_data=self.filterset.data, args=checkboxes_list
                ),
                "has_filter_size": True if self.filterset.data.get("size", None) else False,
                "has_filter_category": True if self.filterset.data.get("category", None) else False,
                "has_filter_price": True
                if (self.filterset.data.get("price_start", None) or self.filterset.data.get("price_end", None))
                else False,
            }
        )
        return context

    def get_queryset(self):
        return Product.objects.prefetch_related(
            "category",
            "translations",
            "category__translations",
            "images",
        ).order_by("-order")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMProductDisableView(DetailView):
    queryset = Product.objects.prefetch_related("translations")

    def get(self, request, *args, **kwargs):
        self.get_object().disable()
        return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMProductEnableView(DetailView):
    queryset = Product.objects.prefetch_related("translations")

    def get(self, request, *args, **kwargs):
        self.get_object().enable()
        return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMProductUpdateView(UpdateView):
    form_class = ProductUpdateForm
    queryset = Product.objects.prefetch_related(
        "translations",
        "category__translations",
        "images",
        "color",
        "color__translations",
    )

    template_name = "crm/products/product.html"
    context_object_name = "product"

    def init_formsets(self):
        if self.request.method == "POST":
            print(self.request.POST)
            self.trade_offers_formset = ProductTradeOffersFormSet(
                self.request.POST, instance=self.get_object(), prefix="trade_offers"
            )
            self.gallery_formset = ProductGalleryFormSet(
                self.request.POST, instance=self.get_object(), prefix="images"
            )
        else:
            self.trade_offers_formset = ProductTradeOffersFormSet(instance=self.get_object(), prefix="trade_offers")
            self.gallery_formset = ProductGalleryFormSet(instance=self.get_object(), prefix="images")

    def get_context_data(self, **kwargs):
        self.object.set_current_language("ru")
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "trade_offers_formset": self.trade_offers_formset,
                "gallery_formset": self.gallery_formset,
            }
        )
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.gallery_formset.save()
        self.trade_offers_formset.save()
        messages.success(self.request, "Товар успешно сохранен")
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.init_formsets()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.init_formsets()
        if form.is_valid() and self.gallery_formset.is_valid() and self.trade_offers_formset.is_valid():
            return self.form_valid(form)
        messages.error(self.request, "Произошла ошибка при сохранении товара")
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("crm:products:product-detail", kwargs={"pk": self.object.pk})


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMProductCreateView(CreateView):
    form_class = ProductUpdateForm
    template_name = "crm/products/product_create.html"

    def init_formsets(self):
        if self.request.method == "POST":
            self.trade_offers_formset = ProductTradeOffersFormSet(self.request.POST, instance=self.object, prefix="trade_offers")
            self.gallery_formset = ProductGalleryFormSet(self.request.POST, instance=self.object, prefix="images")
        else:
            self.trade_offers_formset = ProductTradeOffersFormSet(prefix="trade_offers")
            self.gallery_formset = ProductGalleryFormSet(prefix="images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "trade_offers_formset": self.trade_offers_formset,
                "gallery_formset": self.gallery_formset,
            }
        )
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.init_formsets()
        self.gallery_formset.is_valid()
        self.trade_offers_formset.is_valid()
        self.gallery_formset.save()
        self.trade_offers_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        self.object = None
        self.init_formsets()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.init_formsets()
        if form.is_valid() and self.gallery_formset.is_valid() and self.trade_offers_formset.is_valid():
            return self.form_valid(form)
        print([form.errors for form in self.trade_offers_formset.forms])
        print([form.errors for form in self.gallery_formset.forms])
        print(form.errors)
        messages.error(self.request, "Произошла ошибка при создании товара")
        return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, "Товар успешно создан")
        return reverse_lazy("crm:products:product-detail", kwargs={"pk": self.object.pk})


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMProductDeleteView(DeleteView):
    queryset = Product.objects.all()
    success_url = reverse_lazy("crm:products:products-list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
