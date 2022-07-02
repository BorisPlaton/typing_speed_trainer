from account.models import Profile
from common.form_mixins import CrispyStyleModelFormMixin


class ChangeProfilePhotoForm(CrispyStyleModelFormMixin):
    """Форма изменения фото профиля пользователя."""

    class Meta:
        model = Profile
        fields = ['photo']
