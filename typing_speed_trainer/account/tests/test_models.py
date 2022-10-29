import pytest
from django.db import IntegrityError
from model_bakery import baker

from account.models import User


@pytest.mark.django_db
class TestAccountModels:

    def test_user_creation(self):
        assert not User.objects.all()
        baker.make(User)
        assert len(User.objects.all()) == 1

    def test_create_user_with_existed_email(self):
        credentials = {
            'email': 'test@test.com',
            'password': '12345',
        }
        baker.make(User, **credentials)
        with pytest.raises(IntegrityError):
            baker.make(User, **credentials)
