from django.conf import settings
from django.db import IntegrityError
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

    def test_create_user_with_existed_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                **self.credentials
            )
