from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from account.forms import ChangeProfilePhotoForm
from account.models import User, Profile
from trainer.utils.mixins import TrainerResultCacheMixin


class Account(UpdateView, TrainerResultCacheMixin):
    """Страница профиля пользователя."""
    model = User
    form_class = ChangeProfilePhotoForm
    context_object_name = 'user_profile'
    template_name = 'account/profile.html'

    def dispatch(self, request, *args, **kwargs):
        self.user_pk = kwargs.get('pk')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object.profile
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.get_formatted_results_from_cache()
        return context

    def get_object(self, queryset=None):
        """
        Подключает модели `trainer.models.Statistic`, `account.models.Profile`
        и возвращает объект модели `User`.
        """
        queryset = (self.model.objects
                    .select_related('profile')
                    .select_related('statistic'))
        return super().get_object(queryset)

    def get_formatted_results_from_cache(self) -> list[dict | None]:
        """
        Форматирует значение ключа `dateEnd` в `datetime.datetime`
        и возвращает список со всеми результатами пользователя.
        """
        results = self.get_all_results_from_cache()
        for result in results:
            result['dateEnd'] = datetime.strptime(result['dateEnd'], '%Y-%m-%dT%H:%M:%S.%fZ')
        return results[::-1]


@method_decorator(login_required, name='dispatch')
class DeleteProfilePhoto(UpdateView):
    model = Profile
    fields = ['photo']

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def form_valid(self, form):
        self.object.photo = self.object._meta.get_field('photo').default
        self.object.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.pk == self.kwargs.get('pk'):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseNotAllowed()
