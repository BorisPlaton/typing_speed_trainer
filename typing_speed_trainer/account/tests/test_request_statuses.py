from django.urls import reverse
from model_bakery import baker

from account.models import User
from tests.case_classes.base_case import BaseTestCase


class TestRequestStatuses(BaseTestCase):

    def test_profile_page_200_status_code_with_unauthenticated_user(self, api_client):
        user = baker.make(User)
        response = api_client.get(reverse('account:profile', args=[user.pk]))
        assert response.status_code == 200

    def test_profile_page_200_status_code_with_authenticated_user(self, api_client, user, credentials, login):
        response = api_client.get(reverse('account:profile', args=[user.pk]))
        assert response.status_code == 200

    def test_delete_user_profile_photo_302_status_code_with_unauthenticated_user(self, api_client):
        response = api_client.post(reverse('account:delete_profile_photo'))
        assert response.status_code == 302

    def test_delete_user_profile_photo_302_status_code_with_authenticated_user(
            self, api_client, user, credentials, login
    ):
        response = api_client.post(reverse('account:delete_profile_photo'))
        assert response.status_code == 302
