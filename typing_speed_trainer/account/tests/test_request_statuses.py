from django.test import TestCase
from django.urls import reverse

from account.models import User
from trainer.utils.mixins import TrainerResultCacheMixin


class TestRequestStatuses(TestCase):

    def setUp(self) -> None:
        self.credentials = {
            'email': 'test@test.com',
            'password': '12345'
        }
        self.user = User.objects.create_user(
            **self.credentials,
        )

        self.user_cache_class = TrainerResultCacheMixin()
        self.user_cache_class.user_pk = self.user.pk

    def tearDown(self):
        self.user_cache_class.clean_user_cached_data()

    def test_profile_page_200_status_code_with_unauthenticated_user(self):
        response = self.client.get(reverse('account:profile', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_200_status_code_with_authenticated_user(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('account:profile', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_user_profile_photo_302_status_code_with_unauthenticated_user(self):
        response = self.client.post(reverse('account:delete_profile_photo'))
        self.assertEqual(response.status_code, 302)

    def test_delete_user_profile_photo_302_status_code_with_authenticated_user(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post(reverse('account:delete_profile_photo'))
        self.assertEqual(response.status_code, 302)
