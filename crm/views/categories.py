from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django_filters.views import FilterView

from catalog.models import Category
from crm.filters.categories import CRMCategoriesFilter
from crm.filters.custom_filter import CustomFilter
from crm.forms.category import CategoryUpdateForm
from utils.decorators import crm_member_required


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMCategoriesListView(FilterView, CustomFilter):
    template_name = "crm/categories/categories_list.html"
    paginate_by = 10
    context_object_name = "categories"
    filterset_class = CRMCategoriesFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        checkboxes_list = ["is_active", "is_display_on_main"]
        context.update(
            {
                "disable_categories_url": reverse("crm:api:categories:disable-categories"),
                "enable_categories_url": reverse("crm:api:categories:enable-categories"),
                "delete_categories_url": reverse("crm:api:categories:delete-categories"),
                "copy_categories_url": reverse("crm:api:categories:copy-categories"),
                "has_filter_status": self._get_has_filter_from_checkboxes(
                    filters_data=self.filterset.data, args=checkboxes_list
                ),
            }
        )
        return context

    def get_queryset(self):
        return Category.objects.prefetch_related("translations").order_by("order")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMCategoryChangeStatus(DetailView):
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        self.get_object().change_is_active()
        messages.success(
            self.request,
            "Категория успешно включена" if self.get_object().is_active is True else "Категория успешно выключена"
        )
        return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMCategoryUpdateView(UpdateView):
    queryset = Category.objects.prefetch_related("translations")
    template_name = "crm/categories/category_update.html"
    form_class = CategoryUpdateForm

    def get_success_url(self):
        messages.success(self.request, "Категория успешно обновлена")
        return reverse("crm:categories:category-detail", kwargs={"pk": self.object.pk})


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMCategoryDeleteView(DeleteView):
    queryset = Category.objects.prefetch_related("translations")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Категория успешно удалена")
        return reverse("crm:categories:categories-list")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMCategoryCreateView(CreateView):
    queryset = Category.objects.prefetch_related("translations")
    template_name = "crm/categories/category_create.html"
    form_class = CategoryUpdateForm

    def get_success_url(self):
        messages.success(self.request, "Категория успешно создана")
        return reverse("crm:categories:category-detail", kwargs={"pk": self.object.pk})
