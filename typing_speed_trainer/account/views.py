from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, TemplateView, FormView

from account.forms import RegistrationForm, LoginForm
from account.models import User


class Account(TemplateView):
    """Личный кабинет пользователя."""
    template_name = 'account/profile.html'


class Registration(FormView):
    """Страница регистрации пользователя."""
    template_name = 'registration/registration.html'
    form_class = RegistrationForm


class UserLogin(LoginView):
    """Страница аутентификации пользователя."""
    form_class = LoginForm
