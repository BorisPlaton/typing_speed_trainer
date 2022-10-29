from django.urls import reverse

from tests.case_classes.base_case import BaseTestCase


class TestRequestStatuses(BaseTestCase):

    def test_login_page_200_status_code_with_unauthenticated_user(self, api_client):
        response = api_client.get(reverse('user_auth:login'))
        assert response.status_code == 200

    def test_login_page_302_status_code_with_authenticated_user(self, api_client, login):
        response = api_client.get(reverse('user_auth:login'))
        assert response.status_code == 302

    def test_login_page_302_status_code_with_query_parameters(self, user, api_client, login):
        response = api_client.get(
            reverse('user_auth:login') + '?next=' +
            reverse('account:profile', args=[user.pk])
        )
        assert response.status_code == 302

    def test_registration_page_200_status_code_with_unauthenticated_user(self, api_client):
        response = api_client.get(reverse('user_auth:registration'))
        assert response.status_code == 200

    def test_registration_page_302_status_code_with_authenticated_user(self, api_client, login):
        response = api_client.get(reverse('user_auth:registration'))
        assert response.status_code == 302

    def test_registration_page_302_status_code_with_query_parameters(self, api_client, login):
        response = api_client.get(reverse('user_auth:registration') + '?next=' + reverse('trainer:typing_trainer'))
        assert response.status_code == 302

    def test_reset_password_page_302_status_code_with_authenticated_user(self, api_client, login):
        response = api_client.get(reverse('user_auth:reset_password'))
        assert response.status_code == 302

    def test_reset_password_page_200_status_code_with_unauthenticated_user(self, api_client):
        response = api_client.get(reverse('user_auth:reset_password'))
        assert response.status_code == 200

    def test_logout_page_302_status_with_authenticated_user(self, api_client, login):
        response = api_client.get(reverse('user_auth:logout'))
        assert response.status_code == 302

    def test_logout_page_302_status_with_unauthenticated_user(self, api_client):
        response = api_client.get(reverse('user_auth:logout'))
        assert response.status_code == 302
