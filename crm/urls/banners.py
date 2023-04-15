from django.urls import path
from crm.views.banners import (
    CRMBannersListView,
    CRMSecondBannerListView,
    CRMMainBannerUpdateView,
    CRMSecondBannerUpdateView,
    CRMSecondBannerCreateView,
    CRMSecondBannerChangeStatusView, CRMMainBannersListView, CRMMainBannerCreateView, CRMMainBannerChangeStatusView,
)

app_name = "banners"

urlpatterns = [
    path("list/", CRMBannersListView.as_view(), name="list"),
    # MAIN BANNER
    path("main-banner/list/", CRMMainBannersListView.as_view(), name="main_banner_list"),
    path("main-banner/update/<pk>/", CRMMainBannerUpdateView.as_view(), name="main_banner_update"),
    path("main-banner/create/", CRMMainBannerCreateView.as_view(), name="main_banner_create"),
    path(
        "second-banner/change-status/<pk>/",
        CRMMainBannerChangeStatusView.as_view(),
        name="main-banner-change-status",
    ),
    # SECOND BANNER
    path("second-banner/list/", CRMSecondBannerListView.as_view(), name="second_banner"),
    path("second-banner/update/", CRMSecondBannerUpdateView.as_view(), name="second_banner_update"),
    path("second-banner/create/", CRMSecondBannerCreateView.as_view(), name="second_banner_create"),
    path(
        "second-banner/change-status/<pk>/",
        CRMSecondBannerChangeStatusView.as_view(),
        name="second-banner-change-status",
    ),
    path(
        "second-banner/change-status/<pk>/",
        CRMSecondBannerChangeStatusView.as_view(),
        name="second-banner-delete",
    ),
]
