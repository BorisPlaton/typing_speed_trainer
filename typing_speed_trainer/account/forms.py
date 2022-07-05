from crispy_forms.layout import HTML, Layout, Div, Submit

from account.models import Profile
from common.form_mixins import CrispyStyleModelFormMixin


class ChangeProfilePhotoForm(CrispyStyleModelFormMixin):
    """Форма изменения фото профиля пользователя."""

    class Meta:
        model = Profile
        fields = ['photo']


class ChangeProfileSettingsForm(CrispyStyleModelFormMixin):
    """Форма изменения настроек пользователя."""

    class Meta:
        model = Profile
        fields = ['is_email_shown', 'are_results_shown']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_show_labels = True
        self.helper.field_class = 'mb-2'
        self.helper.layout = Layout(
            *self.get_helper_layout_fields(),
            Div(
                Submit('submit', 'Сохранить', css_class='btn-orange-400 btn-sm'),
                css_class='d-flex justify-content-center mt-3',
            )
        )
