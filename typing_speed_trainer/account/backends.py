from django.contrib.auth.backends import BaseBackend

from account.models import User


class EmailBackend(BaseBackend):
    """
    Кастомный `backend` аутентификации с помощью
    почты.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
