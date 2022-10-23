from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator
from django.forms import modelform_factory
from django.views.generic.base import ContextMixin


class ElidedPaginationMixin:
    pagination_on_each_side = 2
    pagination_on_ends = 2
    paginator_ellipsis = '...'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if paginator := context.get('paginator'):
            paginator: Paginator
            paginator.ELLIPSIS = self.paginator_ellipsis
            context['page_range'] = paginator.get_elided_page_range(
                number=context.get('page_obj').number,
                on_each_side=self.pagination_on_each_side,
                on_ends=self.pagination_on_ends,
            )
        return context


class MultipleFormViewMixin(ContextMixin):
    """
    Mixin for displaying multiple forms, but doesn't respond
    for their processing.
    """

    forms = {}
    forms_on_models = {}
    forms_on_models_fields: dict[str: list | tuple] = {}

    def get_context_data(self, **kwargs):
        """Populates the context with forms."""
        context = super().get_context_data(**kwargs)
        context.update(**self.get_forms())
        return context

    def get_forms(self) -> dict:
        """
        Returns a dictionary with forms as they were
        defined in the `forms` dict.
        """
        self._validate_models_forms()
        initialized_forms = {
            form_name: form(instance=self.object) for form_name, form in self.forms.items()
        }
        for model_name, model in self.forms_on_models.items():
            form = modelform_factory(model, fields=self.forms_on_models_fields.get(model_name))
            initialized_forms.update({model_name: form(instance=self.object)})
        return initialized_forms

    def _validate_models_forms(self) -> bool:
        """Проверяет правильность указания атрибутов `models` и `models_fields`."""
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
