from django.urls import path

from users.views.favorites import FavoritesViewSet

favorites_view_toggle = FavoritesViewSet.as_view({"post": "create"})
favorites_view_list = FavoritesViewSet.as_view({"get": "list"})

urlpatterns = [
    path("toggle/", favorites_view_toggle, name="toggle-favorite"),
    path("list/", favorites_view_list, name="favorites-list"),
]
