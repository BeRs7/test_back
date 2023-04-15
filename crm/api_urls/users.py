from django.urls import path

from crm.api_views.users import DeleteUsersView, CRMChangePassowrd

app_name = "users"

urlpatterns = [
    path("delete/", DeleteUsersView.as_view(), name="delete"),
    path("crm-change-password/<pk>/", CRMChangePassowrd.as_view(), name='change-password'),
]
