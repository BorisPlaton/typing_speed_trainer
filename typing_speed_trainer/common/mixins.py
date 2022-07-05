from django.conf import settings
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic.base import ContextMixin


class UnauthenticatedMixin(View, SuccessURLAllowedHostsMixin):
    """
    Миксин, который проверяет авторизирован пользователь или нет.
    Если так, то перенаправляет на другую страницу.
    """
    redirect_to: str = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self) -> str:
        """Возвращает ссылку для редиректа."""
        redirect_url = resolve_url(self.request.GET.get('next') or self.redirect_to or settings.LOGIN_REDIRECT_URL)

        self.validate_url(redirect_url)

        return redirect_url if self.is_safe_url(redirect_url) else None

    def validate_url(self, url: str):
        """Проверяет корректная ли ссылка. Если нет, вызывает исключение."""
        if url == self.request.path:
            raise ValueError("Ссылка для редиректа ссылается на текущую страницу: %s" % url)
        elif not url:
            raise ValueError(
                "Укажите атрибут `redirect_to`, `settings.LOGIN_REDIRECT_URL` или параметр запроса `next`."
            )

    def is_safe_url(self, url: str) -> bool:
        """Проверяет безопасная ли ссылка, если да, возвращает True, иначе False."""
        url_is_safe = url_has_allowed_host_and_scheme(
            url=url,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return url_is_safe


class SameUserMixin(View):
    """
    Миксин, который проверяет, что действие пользователя, направлено
    на самого себя, иначе возвращает ответ со статусом 403 (Forbidden).
    """

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.pk == self.kwargs.get('pk'):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()


class MultipleFormViewMixin(ContextMixin):
    """Миксин для отображения множества форм. Не отвечает за их обработку."""
    forms = {}
    forms_on_models = {}
    forms_on_models_fields: dict[str: list | tuple] = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**self.get_forms())
        return context

    def get_forms(self) -> dict:
        """
        Возвращает формы в виде словаря с таким же ключом,
        что и в `models`.
        """
        initialized_forms = {}
        self._validate_models_forms()

        for form_name, form in self.forms.items():
            initialized_forms.update({form_name: form(instance=self.object)})

        for model_name, model in self.forms_on_models.items():
            form = modelform_factory(model, fields=self.forms_on_models_fields.get(model_name))
            initialized_forms.update({model_name: form(instance=self.object)})

        return initialized_forms

    def _validate_models_forms(self) -> bool:
        """Проверяет правильность указания атрибутов `models` и `models_fields`."""
        if not (self.forms_on_models or self.forms):
            raise ImproperlyConfigured("Укажите `forms` или `forms_on_models`.")

        for model_name, model in self.forms_on_models.items():

            if model_name not in self.forms_on_models_fields:
                raise ImproperlyConfigured("`{0}` нет в `models_fields`.".format(model_name))

            model_fields = self.forms_on_models_fields.get(model_name)

            if not model_fields:
                raise ImproperlyConfigured("`{0}` не имеет полей в `models_fields`.".format(model_name))

            if not isinstance(model_fields, list | tuple):
                raise ImproperlyConfigured(
                    "Неправильный тип `{0}` у {1} в `models_fields`.".format(type(model_fields), model_name)
                )

            for field in model_fields:
                if not hasattr(model, field):
                    raise ImproperlyConfigured("`{0}` не имеет поля `{1}`.".format(model_name, field))

        return True
