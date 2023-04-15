from django.urls import path

from crm.views.faq import (
    CRMFAQQuestionsListView,
    CRMFAQQuestionUpdateView,
    CRMFAQQuestionCreateView,
    CRMFAQQuestionToggleActiveView,
)
from crm.views.text_pages import (
    CRMTextPagesView,
    CRMTextPagesListView,
    CRMTextPageCreateView,
    CRMTextPageUpdateView,
    CRMTextPageToggleActiveView,
)

app_name = "text-pages"

urlpatterns = [
    path("list/", CRMTextPagesView.as_view(), name="list"),
    path("pages/list/", CRMTextPagesListView.as_view(), name="pages-list"),
    path("pages/create/", CRMTextPageCreateView.as_view(), name="pages-create"),
    path("pages/update/<int:pk>/", CRMTextPageUpdateView.as_view(), name="pages-update"),
    path("pages/toggle-is-active/<int:pk>/", CRMTextPageToggleActiveView.as_view(), name="pages-toggle-is-active"),
    path("faq-questions/list/", CRMFAQQuestionsListView.as_view(), name="questions-list"),
    path("faq-questions/create/", CRMFAQQuestionCreateView.as_view(), name="questions-create"),
    path("faq-questions/update/<int:pk>/", CRMFAQQuestionUpdateView.as_view(), name="questions-update"),
    path(
        "faq-questions/toggle-is-active/<int:pk>/",
        CRMFAQQuestionToggleActiveView.as_view(),
        name="questions-toggle-is-active",
    ),
]
