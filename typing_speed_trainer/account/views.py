from django.contrib.auth.views import LoginView
from django.views.generic import FormView, DetailView

from account.forms import RegistrationForm, LoginForm
from account.models import User
from common.mixins import UnauthenticatedMixin


class Account(DetailView):
    """Личный кабинет пользователя."""
    model = User
    context_object_name = 'user_profile'
    template_name = 'account/profile.html'


class Registration(FormView, UnauthenticatedMixin):
    """Страница регистрации пользователя."""
    template_name = 'registration/registration.html'
    form_class = RegistrationForm


class UserLogin(LoginView):
    """Страница аутентификации пользователя."""
    form_class = LoginForm
    redirect_authenticated_user = True
