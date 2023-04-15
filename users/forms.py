from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from cart.models import Cart
from users.models import User
from utils.forms import StyledForm


class UserAuthForm(AuthenticationForm):
    """
    Форма авторизации менеджера в системе
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Эл. почта",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "Пароль",
            }
        )

    def clean(self):
        cart_pk = self.request.session.get("cart", None)
        cart_products = []
        if type(cart_pk) == list:
            cart_products = cart_pk
            cart_pk = None
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(email__iexact=username).first()
        if user:
            username = user.email
        if User.objects.filter(email__iexact=username, is_active=False).first():
            user = User.objects.filter(email__iexact=username, is_active=False).first()
            # send_activation_email(user)
            raise ValidationError("Осталось только активировать аккаунт, мы отправили вам письмо!")
        if username is not None and password:
            if user and user.type_password != "default":
                raise ValidationError(_("Ваш пароль устарел, необходимо восстановить пароль."))
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
                cart = Cart.objects.filter(Q(pk=cart_pk) | Q(user=user)).last()
                if cart:
                    cart.user = user
                    cart.username = username
                    cart.save(update_fields=("user", "username"))
                    self.request.session["cart"] = cart.pk
                else:
                    cart = Cart.objects.create(user=user, products_json=cart_products)
                    self.request.session["cart"] = cart.pk

        return self.cleaned_data


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
        )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields["email"].widget.attrs.update(
            {
                "placeholder": _("Эл. почта"),
            }
        )
        self.fields["name"].widget.attrs.update(
            {
                "placeholder": _("Имя"),
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": _("Пароль"),
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": _("Подтверждение пароля"),
            }
        )

    def clean(self):
        if User.objects.filter(email=self.cleaned_data.get("email"), is_active=True).exists():
            raise ValidationError(_("Пользователь с таким емейлом уже существует"))
        if not self.cleaned_data.get("name"):
            raise ValidationError(_("Укажите имя"))
        return self.cleaned_data

    def save(self, commit=True):
        if User.objects.filter(email=self.cleaned_data.get("email"), is_active=True).exists():
            raise ValidationError("Email exists")
        elif User.objects.filter(email=self.cleaned_data.get("email"), is_active=False).first():
            user = User.objects.filter(email=self.cleaned_data.get("email")).first()
        else:
            user = super().save(commit=True)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        user.save(update_fields=["is_active"])
        # load_create_client_retail_crm_workload.delay(user.id)
        # send_activation_email(user)
        return user


class UserUpdateForm(forms.ModelForm, StyledForm):
    class Meta:
        model = User
        fields = "__all__"


class UserCreateForm(UserCreationForm, StyledForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "phone_number",
            "is_active",
            "is_staff",
            "is_superuser",
        )
