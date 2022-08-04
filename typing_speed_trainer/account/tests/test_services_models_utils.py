from django.test import TestCase

from account.models import User
from account.services.models_utils import get_users_list_by_statistics
from trainer.models import Statistic


class TestServicesModelsUtils(TestCase):

    def setUp(self) -> None:
        self.first_user = User.objects.create_user('first@email.com', '1')
        self.second_user = User.objects.create_user('second@email.com', '1')

    def set_user_statistic(self, user: User.objects, attempts_amount, wpm, accuracy):
        Statistic.objects.filter(pk=user.statistics.pk).update(
            attempts_amount=attempts_amount,
            wpm=wpm,
            accuracy=accuracy,
        )

    def test_get_users_list_by_statistics_ordering_by_attempts_amount(self):
        self.set_user_statistic(self.first_user, 5, 0, 0)
        self.set_user_statistic(self.second_user, 2, 0, 0)
        users = get_users_list_by_statistics()
        self.assertEqual(self.first_user, users[0])
        self.assertEqual(self.second_user, users[1])

    def test_get_users_list_by_statistics_ordering_by_all_parameters(self):
        self.set_user_statistic(self.first_user, 1, 2, 5)
        self.set_user_statistic(self.second_user, 1, 5, 2)
        users = get_users_list_by_statistics()
        self.assertEqual(self.second_user, users[0])
        self.assertEqual(self.first_user, users[1])

    def test_get_users_list_by_statistics_return_empty_query_set(self):
        User.objects.all().delete()
        self.assertFalse(get_users_list_by_statistics().exists())
