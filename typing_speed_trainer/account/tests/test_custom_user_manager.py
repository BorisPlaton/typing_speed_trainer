from django.test import TestCase

from account.models import User


class TestCustomUserManager(TestCase):

    def setUp(self) -> None:
        self.credentials = {
            'email': 'test@test.com',
            'password': '12345'
        }

    def test_user_creation(self):
        self.assertFalse(User.objects.all())
        User.objects.create_user(**self.credentials)
        self.assertEqual(len(User.objects.all()), 1)
