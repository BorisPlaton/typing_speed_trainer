from datetime import datetime

from django.contrib.auth.views import LoginView
from django.views.generic import FormView, DetailView

from account.forms import RegistrationForm, LoginForm
from account.models import User
from common.mixins import UnauthenticatedMixin
from trainer.utils.mixins import TrainerResultCacheMixin


class Account(DetailView, TrainerResultCacheMixin):
    """Личный кабинет пользователя."""
    model = User
    context_object_name = 'user_profile'
    template_name = 'account/profile.html'

    def dispatch(self, request, *args, **kwargs):
        self.user_pk = kwargs.get('pk')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.get_formatted_results_from_cache()
        return context

    def get_object(self, queryset=None):
        """
        Подключаем модель `trainer.models.Statistic` и
        возвращаем объект `User`.
        """
        print(self.request.user.statistic)
        return super().get_object((self.model.objects.select_related('statistic')))

    def get_formatted_results_from_cache(self) -> list[dict | None]:
        """
        Форматирует значение ключа `dateEnd` в `datetime.datetime`
        и возвращает список со всеми результатами пользователя.
        """
        results = self.get_all_results_from_cache()
        for result in results:
            result['dateEnd'] = datetime.strptime(result['dateEnd'], '%Y-%m-%dT%H:%M:%S.%fZ')
        return results[::-1]


class Registration(FormView, UnauthenticatedMixin):
    """Страница регистрации пользователя."""
    template_name = 'registration/registration.html'
    form_class = RegistrationForm


class UserLogin(LoginView):
    """Страница аутентификации пользователя."""
    form_class = LoginForm
    redirect_authenticated_user = True
