from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms


class CrispyStyleModelFormMixin(forms.ModelForm):
    """Устанавливает стили Django формы."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(*self.get_helper_layout_fields())

    def get_helper_layout_fields(self):
        """Возвращает экземпляр класса `Layout` с настройками полей."""
        fields = []
        for field_name, field in self.fields.items():
            fields.append(
                Field(field_name, autocomplete='off', placeholder=field.label, css_class='mb-2'),
            )

        return fields


class CrispyStyleFormMixin(forms.Form):
    """Устанавливает стили Django формы."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(*self.get_helper_layout_fields())

    def get_helper_layout_fields(self):
        """Возвращает экземпляр класса `Layout` с настройками полей."""
        fields = []
        for field_name, field in self.fields.items():
            fields.append(
                Field(field_name, autocomplete='off', placeholder=field.label, css_class='mb-2'),
            )

        return fields
