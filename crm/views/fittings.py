from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import UpdateView, ListView

from crm.forms.fittings import RegistrationForFittingUpdateForm
from orders.models import RegistrationForFitting
from utils.decorators import crm_member_required


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMFittingsListView(ListView):
    template_name = "crm/fittings/list.html"
    paginate_by = 10
    context_object_name = "registration_fittings"

    def get_queryset(self):
        return RegistrationForFitting.objects.all()


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMFittingUpdateView(UpdateView):
    queryset = RegistrationForFitting.objects.all()
    template_name = "crm/fittings/detail.html"
    form_class = RegistrationForFittingUpdateForm

    def get_success_url(self):
        messages.success(self.request, "Запись успешно обновлена")
        return reverse("crm:fittings:detail", kwargs={"pk": self.object.pk})
