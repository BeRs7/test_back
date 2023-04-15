from pages.models import Page, Vacancy
from pages.models.faq import QuestionCategory, Question
from utils.filters import BaseFilter


class CRMPagesFilter(BaseFilter):

    searching_fields = (
        "id",
        "slug",
        "translations__title",
        "position",
        "is_active",
    )

    class Meta:
        model = Page
        fields = ["id", "translations__title", "position", "is_active", "slug"]


class CRMFaqCategoryFilter(BaseFilter):

    searching_fields = (
        "id",
        "slug",
        "translations__name",
        "translations__title",
        "is_active",
    )

    class Meta:
        model = QuestionCategory
        fields = ["id", "translations__name", "translations__title", "is_active", "slug"]


class CRMFaqQuestionFilter(BaseFilter):

    searching_fields = (
        "id",
        "translations__question",
        "translations__answer",
        "question_category",
        "is_active",
    )

    class Meta:
        model = Question
        fields = ["id", "translations__question", "translations__answer", "is_active", "question_category"]


class CRMVacancyFilter(BaseFilter):

    searching_fields = (
        "city",
        "translations__name",
    )

    class Meta:
        model = Vacancy
        fields = ["city", "translations__name"]
