from django.urls import path

from users.views.cities import UserCityViewSet

app_name = "users_cities"

cities_view_list = UserCityViewSet.as_view({"get": "list"})
cities_view_set = UserCityViewSet.as_view({"post": "create"})

urlpatterns = [
    path("list/", cities_view_list),
    path("set/", cities_view_set),
]
