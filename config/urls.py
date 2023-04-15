from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from config import settings

urlpatterns = [
    path("admin/clearcache/", include("clearcache.urls")),
    path("admin/", admin.site.urls),
    path("crm/", include("crm.urls")),
    path("searchableselect/", include("searchableselect.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [path("api/", include("config.non_multilang_api_urls"))]
urlpatterns += i18n_patterns(path("api/", include("config.api_urls")), prefix_default_language=False)
