from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django import forms
from django.db.models import BooleanField

from service.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Класс формы регистрация пользователя"""

    class Meta:
        model = User
        fields = ["email", "phone", "password1", "password2"]

class CustomPasswordResetForm(PasswordResetForm):
    """Класс для стилизации формы  ввода email для спроса пароля"""

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'my-custom-class',
            'placeholder': 'Введите ваш Email'
        })
    )


