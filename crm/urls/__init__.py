from django.urls import path, include

from crm.views import CRMIndexView
from utils.views import AjaxUploadTempFile

app_name = "crm"

urlpatterns = [
    path("", CRMIndexView.as_view(), name="index"),
    path("", include("crm.urls.utils")),
    path("api/", include("crm.api_urls")),
    path("users/", include("crm.urls.users")),
    path("products/", include("crm.urls.products")),
    path("categories/", include("crm.urls.categories")),
    path("orders/", include("crm.urls.orders")),
    path("fittings/", include("crm.urls.fittings")),
    path("banners/", include("crm.urls.banners")),
    path("colors/", include("crm.urls.colors")),
    path("sizes/", include("crm.urls.sizes")),
    path("text-pages/", include("crm.urls.text_pages")),
    path("tmp-file-upload/", AjaxUploadTempFile.as_view(), name="ajax-file"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]
