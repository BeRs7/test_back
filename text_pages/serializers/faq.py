from rest_framework import serializers

from parler_rest.fields import TranslatedFieldsField

from text_pages.models import FAQQuestion


class FAQQuestionSerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=FAQQuestion)

    class Meta:
        model = FAQQuestion
        fields = ("translations",)
