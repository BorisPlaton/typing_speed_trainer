from django.urls import reverse

from tests.utils import BaseTestCase


class TestRequestStatuses(BaseTestCase):

    def test_typing_trainer_page_200_status_code_with_unauthenticated_user(self, api_client):
        response = api_client.get(reverse('trainer:typing_trainer'))
        assert response.status_code == 200

    def test_typing_trainer_page_200_status_code_with_authenticated_user(self, api_client, login):
        response = api_client.get(reverse('trainer:typing_trainer'))
        assert response.status_code == 200
