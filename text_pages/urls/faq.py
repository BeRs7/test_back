from django.urls import path

from text_pages.views.faq import FAQQuestionsListPage

app_name = "faq"

urlpatterns = [
    path("", FAQQuestionsListPage.as_view(), name="faq"),
]
