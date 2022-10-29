import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from account.models import User


class CacheTestCase:
    """Makes setup and teardown stuff for cache."""

    def teardown_method(self, method):
        """Cleans a test cache database."""
        cache.clear()


class APITestCase:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def credentials(self):
        return {
            'email': 'test@test.com',
            'password': '12345',
        }

    @pytest.fixture
    def user(self, credentials):
        return User.objects.create_user(**credentials)

    @pytest.fixture
    def login(self, api_client, credentials):
        assert api_client.login(**credentials)


@pytest.mark.django_db
class BaseTestCase(CacheTestCase, APITestCase):
    pass
