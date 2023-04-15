from django.urls import path

from crm.views.users import (
    CRMLoginView,
    CRMLogoutView,
    CRMUsersListView,
    CRMUsersUpdateView,
    CRMUsersDeleteView,
    CRMUsersCreateView,
)

app_name = "users"

urlpatterns = [
    path("list/", CRMUsersListView.as_view(), name="list"),
    path("detail/<pk>/", CRMUsersUpdateView.as_view(), name="detail"),
    path("delete/<pk>/", CRMUsersDeleteView.as_view(), name="delete"),
    path("create/", CRMUsersCreateView.as_view(), name="create"),
    path("login/", CRMLoginView.as_view(), name="login"),
    path("logout/", CRMLogoutView.as_view(), name="logout"),
]
