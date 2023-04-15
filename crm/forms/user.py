from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from users.models import User
from utils.forms import StyledForm
from django import forms


class CRMAuthForm(AuthenticationForm, StyledForm):
    """
    Форма авторизации менеджера в системе
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "label": "Логин",
                "placeholder": "Введите логин",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "label": "Пароль",
                "placeholder": "Введите пароль",
            }
        )

    def get_invalid_login_error(self):
        return ValidationError("Неверный имя пользователя или пароль")

    def clean(self):
        super().clean()
        # Проверка: Пользователь может зайти в CRM систему
        username = self.cleaned_data.get("username")
        user = User.objects.filter(email=username).first()
        if user and not user.is_can_access_crm:
            self.add_error(None, "Нет прав для входа")
        return self.cleaned_data


class CRMUserUpdateForm(forms.ModelForm, StyledForm):
    class Meta:
        model = User
        fields = ["email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "is_superuser"]
