from django.urls import path

from crm.api_views.banners import DeleteSecondBannerView, DeleteMainBannerView


app_name = "banners"

urlpatterns = [
    path("second/delete/", DeleteSecondBannerView.as_view(), name="second-banner-delete"),
    path("main/delete/", DeleteMainBannerView.as_view(), name="main-banner-delete"),
]
