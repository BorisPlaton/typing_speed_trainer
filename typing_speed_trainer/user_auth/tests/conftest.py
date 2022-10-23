import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture(autouse=True)
def user(credentials):
    return User.objects.create_user(**credentials)
