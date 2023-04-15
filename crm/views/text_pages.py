from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DetailView

from crm.forms.text_pages import CRMTextPageCreationForm
from text_pages.models import TextPage
from utils.decorators import crm_member_required


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMTextPagesView(TemplateView):
    template_name = "crm/text_pages/list.html"


class CRMTextPagesListView(ListView):
    template_name = "crm/text_pages/text_pages/text_pages_list.html"
    context_object_name = "pages"

    def get_queryset(self):
        return TextPage.objects.all()


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMTextPageCreateView(CreateView):
    form_class = CRMTextPageCreationForm
    template_name = "crm/text_pages/text_pages/create.html"
    queryset = TextPage.objects.all()

    def get_success_url(self):
        return reverse_lazy("crm:text-pages:pages-list")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMTextPageUpdateView(UpdateView):
    template_name = "crm/text_pages/text_pages/update.html"
    context_object_name = "page"
    form_class = CRMTextPageCreationForm

    def get_queryset(self):
        return TextPage.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Страница успешно сохранена")
        return reverse_lazy("crm:text-pages:pages-update", kwargs={"pk": self.kwargs.get("pk")})


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMTextPageToggleActiveView(DetailView):
    template_name = "crm/text_pages/text_pages/update.html"
    queryset = TextPage.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()  # type: TextPage
        obj.is_active = not obj.is_active
        obj.save(update_fields=("is_active",))
        state = "включена" if obj.is_active else "выключена"
        messages.success(self.request, "Страница успешно {}".format(state))
        return redirect(request.META.get("HTTP_REFERER"))
