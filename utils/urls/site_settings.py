from django.urls import path

from utils.views.sitesettings import SiteSettingsAPIView

app_name = 'site_settings'

urlpatterns = [
    path("", SiteSettingsAPIView.as_view(), name='settings'),
]
