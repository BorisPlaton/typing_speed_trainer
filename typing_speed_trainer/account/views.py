from datetime import datetime

from django.views.generic.detail import DetailView
from sorl.thumbnail import delete
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from account.forms import ChangeProfilePhotoForm, ChangeProfileSettingsForm
from account.models import Profile
from common.mixins import MultipleFormViewMixin, ResultsFormattingMixin
from trainer.utils.cache_results import TrainerResultCache


class Account(DetailView, ResultsFormattingMixin, MultipleFormViewMixin, TrainerResultCache):
    """Страница профиля пользователя."""

    model = Profile
    context_object_name = 'user_profile'
    template_name = 'account/profile.html'

    forms = {
        'load_photo_form': ChangeProfilePhotoForm,
        'user_settings_form': ChangeProfileSettingsForm,
    }
    forms_on_models = {
        'delete_photo_form': Profile,
    }
    forms_on_models_fields = {
        'delete_photo_form': ['photo'],
    }

    def dispatch(self, request, *args, **kwargs):
        """
        Устанавливаем значение атрибута `user_pk` равным полю `id`
        пользователя, для корректной работы миксина `TrainerResultCacheMixin`.
        """
        self.user_id = kwargs.get('pk')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Наполняем контекст шаблонов своими данными."""
        context = super().get_context_data(**kwargs)
        context['results'] = self.get_formatted_results_from_cache()
        context['has_default_photo'] = (
                self.object._meta.get_field('photo').default == self.object.photo
        )
        return context

    def get_object(self, queryset=None):
        """
        Подключает модели `trainer.models.Statistic`, `account.models.Profile`
        и возвращает объект модели `User`.
        """
        queryset = (self.model.objects
                    .select_related('user')
                    .select_related('user__statistic'))
        return super().get_object(queryset)

    def get_formatted_results_from_cache(self) -> list[dict | None]:
        """
        Форматирует значение ключа `dateEnd` в `datetime.datetime`
        и возвращает список со всеми результатами пользователя.
        """
        return self.get_formatted_date_end_results(
            self.get_all_current_user_results()
        )


@method_decorator(login_required, name='dispatch')
class UpdateProfileSettings(UpdateView):
    """View-класс для изменения настроек пользователя."""

    model = Profile
    fields = ['is_email_shown', 'are_results_shown']

    def get_object(self, queryset=None):
        return self.request.user.profile


@method_decorator(login_required, name='dispatch')
class UpdateProfilePhoto(UpdateView):
    """View-класс для загрузки нового фото пользователя."""

    model = Profile
    fields = ['photo']

    def get_object(self, queryset=None):
        return self.request.user.profile


@method_decorator(login_required, name='dispatch')
class DeleteProfilePhoto(UpdateView):
    """View-класс для удаления фото пользователя."""

    model = Profile
    fields = ['photo']

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        default_photo = self.object._meta.get_field('photo').default
        if self.object.photo != default_photo:
            delete(self.object.photo)
            self.object.photo = default_photo
            self.object.save()
        return super().form_valid(form)
