import pytest
from django.core.cache import cache
from rest_framework.test import APIClient


@pytest.mark.django_db
class BaseTestCase:

    def teardown_method(self, method):
        cache.clear()

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
    def login(self, api_client, credentials):
        assert api_client.login(**credentials)
