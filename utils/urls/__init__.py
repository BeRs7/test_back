from django.urls import path, include

from utils.views import TempFileUploader
from utils.views.general import GeneralAPIView
from utils.views.main_page import MainPageView


app_name = "utils"

urlpatterns = [
    path("banners/", include("utils.urls.banners")),
    path("main-page/", MainPageView.as_view()),
    path("general/", GeneralAPIView.as_view()),
    path("site-settings/", include("utils.urls.site_settings")),
    path("temp-file/", TempFileUploader.as_view()),
]
