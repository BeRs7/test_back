from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from crm.forms.faq import CRMFAQQuestionCreationForm
from text_pages.models import FAQQuestion
from utils.decorators import crm_member_required


class CRMFAQQuestionsListView(ListView):
    template_name = "crm/text_pages/faq/list.html"
    context_object_name = "questions"

    def get_queryset(self):
        return FAQQuestion.objects.all()


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMFAQQuestionCreateView(CreateView):
    form_class = CRMFAQQuestionCreationForm
    template_name = "crm/text_pages/faq/create.html"
    queryset = FAQQuestion.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Вопрос-ответ успешно создан")
        return reverse_lazy("crm:text-pages:questions-list")


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMFAQQuestionUpdateView(UpdateView):
    template_name = "crm/text_pages/faq/update.html"
    context_object_name = "page"
    form_class = CRMFAQQuestionCreationForm

    def get_queryset(self):
        return FAQQuestion.objects.all()

    def get_success_url(self):
        messages.success(self.request, "Вопрос-ответ успешно отредактирован")
        return reverse_lazy("crm:text-pages:questions-update", kwargs={"pk": self.kwargs.get("pk")})


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMFAQQuestionToggleActiveView(DetailView):
    template_name = "crm/text_pages/faq/update.html"
    queryset = FAQQuestion.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()  # type: FAQQuestion
        obj.is_active = not obj.is_active
        obj.save(update_fields=("is_active",))
        state = "включен" if obj.is_active else "выключен"
        messages.success(self.request, "Вопрос-ответ успешно {}".format(state))
        return redirect(request.META.get("HTTP_REFERER"))
