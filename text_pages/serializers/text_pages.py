from parler_rest.fields import TranslatedFieldsField
from rest_framework import serializers

from text_pages.models import TextPage


class TextPageTranslationSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    seo_title = serializers.CharField()
    seo_content = serializers.CharField()

    class Meta:
        model = TextPage
        fields = ("title", "seo_title", "seo_content")


class TextPageSerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(serializer_class=TextPageTranslationSerializer, shared_model=TextPage)

    class Meta:
        model = TextPage
        fields = ("translations", "slug", "menu_position", "show_in_footer")


class DetailTextPageTranslationSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    seo_title = serializers.CharField()
    seo_content = serializers.CharField()

    class Meta:
        model = TextPage
        fields = ("title", "seo_title", "seo_content", "content", "show_in_footer")


class DetailTextPageSerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(serializer_class=DetailTextPageTranslationSerializer, shared_model=TextPage)

    class Meta:
        model = TextPage
        fields = ("translations", "slug", "menu_position", "show_in_footer")
