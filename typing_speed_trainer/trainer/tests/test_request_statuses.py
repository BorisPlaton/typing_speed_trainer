import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker

from tests.case_classes.base_case import BaseTestCase


User = get_user_model()


class TestRequestStatuses(BaseTestCase):

    @pytest.fixture(autouse=True)
    def create_user(self, credentials):
        baker.make(User)

    def test_typing_trainer_page_200_status_code_with_unauthenticated_user(self, api_client):
        response = api_client.get(reverse('trainer:typing_trainer'))
        assert response.status_code == 200

    def test_typing_trainer_page_200_status_code_with_authenticated_user(self, api_client, user, login):
        response = api_client.get(reverse('trainer:typing_trainer'))
        assert response.status_code == 200
