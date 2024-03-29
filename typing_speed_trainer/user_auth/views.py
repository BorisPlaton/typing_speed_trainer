from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user_auth.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordResetConfirmForm
from common.mixins import UnauthenticatedMixin


class UserRegistration(CreateView, UnauthenticatedMixin):
    """The register page."""

    template_name = 'user_auth/registration.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='account.backends.EmailBackend')
        return response


class UserLogin(LoginView):
    """The authentication page."""

    form_class = LoginForm
    template_name = 'user_auth/login.html'
    redirect_authenticated_user = True


class UserPasswordReset(PasswordResetView, UnauthenticatedMixin):
    """The page for user's password recovery."""

    form_class = UserPasswordResetForm
    success_url = reverse_lazy('user_auth:login')
    email_template_name = 'user_auth/password_reset_email.html'
    template_name = 'user_auth/user_password_reset_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Письмо было отправлено")
        return super().form_valid(form)


class UserPasswordResetConfirm(PasswordResetConfirmView, UnauthenticatedMixin):
    """
    The page for the password change. It is used via special link
    that is sent on user's email.
    """

    form_class = UserPasswordResetConfirmForm
    template_name = 'user_auth/user_password_reset_confirm.html'
    success_url = reverse_lazy('user_auth:login')

    def form_valid(self, form):
        messages.success(self.request, "Пароль был успешно изменён")
        return super().form_valid(form)
