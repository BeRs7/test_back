from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from phonenumber_field.phonenumber import to_python
from rest_framework.fields import EmailField


class PhoneNumberField(serializers.CharField):
    default_error_messages = {"invalid": _("Неправильный формат номера телефона.")}

    def to_internal_value(self, data):
        phone_number = to_python(data)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages["invalid"])
        return phone_number


class UsernameField(EmailField):
    def __init__(self, **kwargs):
        super(EmailField, self).__init__(**kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return value.strip().lower()
