from django.urls import include, path

app_name = "users"

urlpatterns = [
    path("favorites/", include("users.urls.favorites")),
    path("cities/", include("users.urls.cities")),
]
