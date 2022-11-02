from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from account.models import User
from common.form_mixins import CrispyStyleModelFormMixin, CrispyStyleFormMixin


class RegistrationForm(CrispyStyleModelFormMixin):
    """The registration form."""

    repeat_password = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'repeat_password']

        error_messages = {
            'email': {
                'unique': "Пользователь с такой почтой уже существует.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    def clean_repeat_password(self):
        """Checks if passwords match each other."""
        if self.cleaned_data['repeat_password'] != self.cleaned_data['password']:
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data['repeat_password']

    def save(self, commit=True):
        instance: User = super().save(commit=False)
        instance.set_password(instance.password)
        instance.save()
        return instance


class LoginForm(AuthenticationForm, CrispyStyleFormMixin):
    """The authentication form."""

    username = forms.EmailField(label="Почта")

    error_messages = {
        "invalid_login": "Введите правильную почту и пароль.",
        "inactive": "Этот аккаунт неактивен.",
    }


class UserPasswordResetForm(PasswordResetForm, CrispyStyleFormMixin):
    """
    Форма сброса пароля. Для восстановления пароля использует
    почту пользователя.
    """


class UserPasswordResetConfirmForm(SetPasswordForm, CrispyStyleFormMixin):
    """
    Форма для изменения пароля. Для восстановления пароля использует
    почту пользователя.
    """

    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(),
        strip=False,
    )
