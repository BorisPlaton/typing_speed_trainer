import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture
def user(credentials):
    return User.objects.create_user(**credentials)


@pytest.fixture
def second_user(credentials):
    new_credentials = dict(credentials)
    new_credentials.update({'email': 'second_user@email.com'})
    return User.objects.create_user(**new_credentials)
