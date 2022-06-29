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

    def test_typing_trainer_page_200_status_code_with_unauthenticated_user(self):
        response = self.client.get(reverse('trainer:typing_trainer'))
        self.assertEqual(response.status_code, 200)

    def test_typing_trainer_page_200_status_code_with_authenticated_user(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('trainer:typing_trainer'))
        self.assertEqual(response.status_code, 200)
