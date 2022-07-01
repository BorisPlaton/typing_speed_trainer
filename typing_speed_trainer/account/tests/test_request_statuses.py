from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from account.models import User


class TestRequestStatuses(TestCase):

    def setUp(self) -> None:
        self.credentials = {
            'email': 'test@test.com',
            'password': '12345'
        }
        self.user = User.objects.create_user(
            **self.credentials,
        )

    def test_login_page_200_status_code_with_unauthenticated_user(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_302_status_code_with_authenticated_user(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('account:login'))
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_login_page_302_status_code_with_query_parameters(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(
            reverse('account:login') + '?next=' + reverse('account:profile', args=[self.user.pk]))
        self.assertRedirects(response, reverse('account:profile', args=[self.user.pk]))

    def test_registration_page_200_status_code_with_unauthenticated_user(self):
        response = self.client.get(reverse('account:user_auth'))
        self.assertEqual(response.status_code, 200)

    def test_registration_page_302_status_code_with_authenticated_user(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('account:user_auth'))
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_registration_page_302_status_code_with_query_parameters(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('account:user_auth') + '?next=' + reverse('trainer:typing_trainer'))
        self.assertRedirects(response, reverse('trainer:typing_trainer'))

    def test_profile_page_200_status_code_with_unauthenticated_user(self):
        response = self.client.get(reverse('account:profile', args=[self.user.pk]))
        self.assertTrue(response.status_code, 200)

    def test_profile_page_200_status_code_with_authenticated_user(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('account:profile', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
