from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_filters.views import FilterView

from crm.filters.banners import CRMBannersFilter, CRMMainBannersFilter
from crm.forms.banner import CRMMainBannerUpdateForm, CRMSecondUpdateCreateForm
from utils.decorators import crm_member_required
from utils.models import MainBanner, SecondBanner


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMBannersListView(ListView):
    template_name = "crm/banners/list.html"

    def get_queryset(self):
        return MainBanner.objects.all()


# MAIN_BANNER
@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMMainBannersListView(FilterView):
    template_name = "crm/banners/main_banner/main_banner_list.html"
    context_object_name = "banners"
    filterset_class = CRMMainBannersFilter

    def get_queryset(self):
        return MainBanner.objects.order_by("order")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({"main_banner_delete_url": reverse("crm:api:banners:main-banner-delete")})
        return context


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMMainBannerUpdateView(UpdateView):
    template_name = "crm/banners/main_banner/main_banner_update.html"
    queryset = MainBanner.objects.all()
    context_object_name = "banner"
    form_class = CRMMainBannerUpdateForm

    def get_success_url(self):
        messages.success(self.request, "Баннер успешно сохранен")
        return reverse_lazy("crm:banners:main_banner_update", kwargs={"pk": self.object.pk})


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMMainBannerCreateView(CreateView):
    form_class = CRMMainBannerUpdateForm
    template_name = "crm/banners/main_banner/main_banner_create.html"
    queryset = MainBanner.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Баннер успешно создан")
        return reverse_lazy("crm:banners:main_banner_list")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMMainBannerChangeStatusView(DetailView):
    queryset = MainBanner.objects.all()

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        status = "выключен" if object.is_active else "включен"
        object.change_status()
        messages.success(self.request, "Баннер успешно " + status)
        return redirect(request.META.get("HTTP_REFERER"))


# SECOND BANNER
@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMSecondBannerListView(FilterView):
    template_name = "crm/banners/second_banner/second_banner_list.html"
    context_object_name = "banners"
    filterset_class = CRMBannersFilter

    def get_queryset(self):
        return SecondBanner.objects.order_by("-id")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({"second_banner_delete_url": reverse("crm:api:banners:second-banner-delete")})
        return context


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMSecondBannerUpdateView(UpdateView):
    template_name = "crm/banners/second_banner/second_banner_update.html"
    context_object_name = "banners"
    filterset_class = CRMBannersFilter
    form_class = CRMSecondUpdateCreateForm

    def get_object(self, queryset=None):
        obj = SecondBanner.get_solo()
        obj.safe_translation_getter('title')
        return obj

    def get_success_url(self):
        messages.success(self.request, "Баннер успешно сохранен")
        return reverse_lazy("crm:banners:second_banner_update")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMSecondBannerCreateView(CreateView):
    form_class = CRMSecondUpdateCreateForm
    template_name = "crm/banners/second_banner/second_banner_create.html"
    queryset = SecondBanner.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Баннер успешно создан")
        return reverse_lazy("crm:banners:second_banner")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMSecondBannerChangeStatusView(DetailView):
    queryset = SecondBanner.objects.all()

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        status = "выключен" if object.is_active else "включен"
        object.change_status()
        messages.success(self.request, "Баннер успешно " + status)
        return redirect(request.META.get("HTTP_REFERER"))
