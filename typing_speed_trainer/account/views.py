from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from account.forms import RegistrationForm, LoginForm
from common.mixins import UnauthenticatedMixin


@method_decorator(login_required, name='dispatch')
class Account(TemplateView):
    """Личный кабинет пользователя."""
    template_name = 'account/profile.html'


class Registration(FormView, UnauthenticatedMixin):
    """Страница регистрации пользователя."""
    template_name = 'registration/registration.html'
    form_class = RegistrationForm


class UserLogin(LoginView):
    """Страница аутентификации пользователя."""
    form_class = LoginForm
    redirect_authenticated_user = True
