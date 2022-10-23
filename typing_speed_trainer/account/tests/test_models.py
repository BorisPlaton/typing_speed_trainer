import pytest
from django.db import IntegrityError

from account.models import User


@pytest.mark.django_db
class TestAccountModels:

    @pytest.fixture
    def credentials(self):
        return {
            'email': 'test@test.com',
            'password': '12345',
        }

    def test_user_creation(self, credentials):
        assert not User.objects.all()
        User.objects.create_user(**credentials)
        assert len(User.objects.all()) == 1

    def test_create_user_with_existed_email(self, credentials, user):
        with pytest.raises(IntegrityError):
            User.objects.create_user(**credentials)
