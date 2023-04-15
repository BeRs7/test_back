from django.urls import path

from utils.views import SaleBannerListView, MainBannerListView
from utils.views.page_404 import Page404DetailView

urlpatterns = [
    path("main/", MainBannerListView.as_view(), name="main-banners-list"),
    path("second/", SaleBannerListView.as_view(), name="sale-banners-list"),
    path("404/", Page404DetailView.as_view(), name="404-page"),
]
