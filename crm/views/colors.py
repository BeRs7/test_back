from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from crm.forms.colors import CRMColorColorCreationForm
from utils.decorators import crm_member_required
from catalog.models import Color


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMColorsListView(ListView):
    template_name = "crm/colors/list.html"
    context_object_name = "colors"

    def get_queryset(self):
        return Color.objects.all().order_by("id").distinct("id")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMColorCreateView(CreateView):
    form_class = CRMColorColorCreationForm
    template_name = "crm/colors/create.html"
    queryset = Color.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Цвет успешно создан")
        return reverse_lazy("crm:colors:list")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMColorUpdateView(UpdateView):
    template_name = "crm/colors/update.html"
    context_object_name = "page"
    form_class = CRMColorColorCreationForm

    def get_queryset(self):
        return Color.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Цвет успешно сохранен")
        return reverse_lazy("crm:colors:update", kwargs={"pk": self.kwargs.get("pk")})


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMColorToggleActiveView(DetailView):
    template_name = "crm/colors/update.html"
    queryset = Color.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()  # type: Color
        obj.display_on_main = not obj.display_on_main
        obj.save(update_fields=("display_on_main",))
        state = "включен" if obj.display_on_main else "выключен"
        messages.success(self.request, "Показ цвета в шапке успешно {}".format(state))
        return redirect(request.META.get("HTTP_REFERER"))


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMColorDeleteView(DetailView):
    template_name = "crm/colors/update.html"
    queryset = Color.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()  # type: Color
        obj.delete()
        messages.success(self.request, "Цвет удален")
        return redirect(request.META.get("HTTP_REFERER"))
