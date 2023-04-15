from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache

from utils.decorators import crm_member_required


@method_decorator(crm_member_required, "dispatch")
@method_decorator(never_cache, "dispatch")
class CRMGlobalSearchView(generic.TemplateView):
    template_name = "crm/utils/global_search.html"
