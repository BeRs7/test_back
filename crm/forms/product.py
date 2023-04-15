from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.forms import inlineformset_factory
from parler.forms import TranslatedField
from django_select2 import forms as s2forms

from catalog.models import Category, Product, ProductTag, Color, TradeOffer, Size
from catalog.models.product import ProductGallery
from utils.forms import BaseTranslatedModelForm, StyledForm

from utils.models.temp_file import TempFile


class SuggestedWidget(s2forms.ModelSelect2MultipleWidget):
    queryset = Product.objects.prefetch_related("translations", "images")
    search_fields = ["translations__name__icontains"]


class ColorsWidget(s2forms.ModelSelect2MultipleWidget):
    queryset = Product.objects.prefetch_related("translations", "images")
    search_fields = ["translations__name__icontains"]


class CategoryWidget(s2forms.ModelSelect2MultipleWidget):
    queryset = Category.objects.all()
    search_fields = ["translations__name__icontains"]


class MajorCategoryWidget(s2forms.ModelSelect2Widget):
    queryset = Category.objects.all()
    search_fields = ["translations__name__icontains"]


class TotalLookWidget(s2forms.ModelSelect2MultipleWidget):
    queryset = Product.objects.active()
    search_fields = ["translations__name__icontains"]


class TagsWidget(s2forms.ModelSelect2MultipleWidget):
    queryset = ProductTag.objects.filter(is_active=True).prefetch_related("translations")
    search_fields = ["translations__text__icontains"]


class SeoTagsWidget(s2forms.ModelSelect2MultipleWidget):
    queryset = ProductTag.objects.filter(is_active=True).prefetch_related("translations")
    search_fields = ["translations__text__icontains"]


class ColorWidget(s2forms.ModelSelect2Widget):
    queryset = Color.objects.all().prefetch_related("translations")
    search_fields = ["translations__name"]


class SizeWidget(s2forms.ModelSelect2Widget):
    queryset = Size.objects.all().prefetch_related("translations")
    search_fields = ["translations__size"]


class ProductUpdateForm(BaseTranslatedModelForm):
    name = TranslatedField()
    style_after_init_hook = True
    length = forms.IntegerField(label="Длина", required=False)
    weight = forms.IntegerField(label="Вес в граммах", required=False)
    width = forms.IntegerField(label="Ширина", required=False)
    height = forms.IntegerField(label="Высота", required=False)
    widgets = {
        "name": forms.CharField(max_length=200, label="Название", required=False),
        "description": forms.CharField(label="Описание", widget=CKEditorUploadingWidget(), required=False),
        "model_measurements": forms.CharField(label="Обмеры модели", widget=CKEditorUploadingWidget(), required=False),
        "composition_and_care": forms.CharField(label="Состав и уход", widget=CKEditorUploadingWidget(), required=False),
    }

    class Meta:
        model = Product
        fields = (
            "slug",
            "video",
            "is_active",
            "is_new",
            "order",
            "category",
            "major_category",
            "price",
            "price_with_sale",
            "color",
            "colors",
            "width",
            "height",
            "length",
            "weight",
            "suggested_products",
            "tags",
            "seo_tags",
            "total_look",
            "sku",
        )
        multiple_languages_fields = (
            "name",
            "description",
            "model_measurements",
            "composition_and_care",
        )
        exclude = multiple_languages_fields
        widgets = {
            "suggested_products": SuggestedWidget,
            "category": CategoryWidget,
            "major_category": MajorCategoryWidget,
            "tags": TagsWidget,
            "seo_tags": SeoTagsWidget,
            "total_look": TotalLookWidget,
            "color": ColorWidget,
            "colors": ColorsWidget,
        }

    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields["color"].queryset = self.fields["color"].queryset.prefetch_related("translations")


class ProductGalleryForm(forms.ModelForm):
    temp_file = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "js-temp-file"}))

    class Meta:
        model = ProductGallery
        fields = ["temp_file", "product", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order"].widget.attrs.update({"class": "js-order-field"})

    def save(self, commit=True):
        temp_file_id = self.cleaned_data.pop("temp_file", None)
        if temp_file_id:
            temp_file = TempFile.objects.get(pk=temp_file_id)
            instance = super().save(False)
            instance.file = temp_file.file
            instance.save()
        else:
            instance = super().save(commit)
        return instance


class ProductTradeOfferForm(forms.ModelForm, StyledForm):
    style_after_init_hook = True
    size = forms.ModelChoiceField(label="", widget=SizeWidget, queryset=Size.objects.all())
    amount = forms.IntegerField(label="", min_value=0)
    is_active = forms.BooleanField(label="", required=False)
    DELETE = forms.BooleanField(label="", required=False)

    class Meta:
        model = TradeOffer
        fields = ("size", "is_active", "amount", "DELETE")
        widgets = {
            "size": SizeWidget,
        }


ProductTradeOffersFormSet = inlineformset_factory(
    model=TradeOffer, form=ProductTradeOfferForm, parent_model=Product, extra=0, can_delete=True
)


ProductGalleryFormSet = inlineformset_factory(
    model=ProductGallery,
    form=ProductGalleryForm,
    parent_model=Product,
    extra=0,
    can_delete=True,
)
