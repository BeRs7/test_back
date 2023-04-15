from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.views import auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, UpdateView, CreateView, DeleteView
from django_filters.views import FilterView

from crm.filters.users import CRMUsersFilter
from crm.forms.user import CRMAuthForm
from users.forms import UserCreateForm
from crm.forms.user import CRMUserUpdateForm
from users.models import User
from utils.decorators import crm_member_required


class CRMLoginView(LoginView):
    form_class = CRMAuthForm
    template_name = "crm/users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("crm:index")


@method_decorator(crm_member_required, "dispatch")
class CRMLogoutView(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(reverse_lazy("crm:users:login"))


@method_decorator(crm_member_required, "dispatch")
class CRMUsersListView(FilterView):
    template_name = "crm/users/users_list.html"
    paginate_by = 50
    context_object_name = "users"
    queryset = User.objects.all()
    filterset_class = CRMUsersFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(
            {
                "delete_users_url": reverse("crm:api:users:delete"),
            }
        )
        return context


@method_decorator(crm_member_required, "dispatch")
class CRMUsersUpdateView(UpdateView):
    template_name = "crm/users/user_update.html"
    queryset = User.objects.all()
    context_object_name = "user"
    form_class = CRMUserUpdateForm

    def get_success_url(self):
        return reverse_lazy("crm:users:detail", kwargs={"pk": self.kwargs.get("pk")})


@method_decorator(crm_member_required, "dispatch")
class CRMUsersCreateView(UserPassesTestMixin, CreateView):
    template_name = "crm/users/user_create.html"
    model = User
    form_class = UserCreateForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse_lazy("crm:users:detail", kwargs={"pk": self.object.pk}))

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


@method_decorator(crm_member_required, "dispatch")
class CRMUsersDeleteView(DeleteView):
    queryset = User.objects.all()
    success_url = reverse_lazy("crm:users:list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
