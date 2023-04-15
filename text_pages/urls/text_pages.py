from django.urls import path

from text_pages.views import TextPagesMainPage, TextPagesListPage

app_name = "text_pages"

urlpatterns = [
    path("detail/<slug:slug>/", TextPagesMainPage.as_view(), name="text-page-detail"),
    path("list/", TextPagesListPage.as_view(), name="text-page-list"),
]
