from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from crm.forms.sizes import CRMSizesCreationForm
from utils.decorators import crm_member_required
from catalog.models import Color, Size


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMSizesListView(ListView):
    template_name = "crm/sizes/list.html"
    context_object_name = "sizes"

    def get_queryset(self):
        return Size.objects.all().order_by("id").distinct("id")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMSizeCreateView(CreateView):
    form_class = CRMSizesCreationForm
    template_name = "crm/sizes/create.html"
    queryset = Size.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Размер успешно создан")
        return reverse_lazy("crm:sizes:list")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMSizeUpdateView(UpdateView):
    template_name = "crm/sizes/update.html"
    context_object_name = "page"
    form_class = CRMSizesCreationForm

    def get_queryset(self):
        return Size.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Размер успешно сохранен")
        return reverse_lazy("crm:sizes:update", kwargs={"pk": self.kwargs.get("pk")})


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMSizeToggleActiveView(DetailView):
    template_name = "crm/sizes/update.html"
    queryset = Size.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()  # type: Color
        obj.display_on_main = not obj.display_on_main
        obj.save(update_fields=("display_on_main",))
        state = "включен" if obj.display_on_main else "выключен"
        messages.success(self.request, "Показ размера в шапке успешно {}".format(state))
        return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMSizeDeleteView(DetailView):
    template_name = "crm/sizes/update.html"
    queryset = Size.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()  # type: Color
        obj.delete()
        messages.success(self.request, "Размер удален")
        return redirect(request.META.get("HTTP_REFERER"))
