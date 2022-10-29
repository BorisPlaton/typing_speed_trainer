import pytest
from model_bakery import baker

from account.models import User
from account.selectors import get_users_list_by_statistics
from tests.case_classes.base_case import CacheTestCase
from trainer.models import Statistic


@pytest.mark.django_db
class TestServicesModelsUtils(CacheTestCase):

    @staticmethod
    def set_user_statistic(user: User, attempts_amount, wpm, accuracy):
        Statistic.objects.filter(pk=user.statistics.pk).update(
            attempts_amount=attempts_amount,
            wpm=wpm,
            accuracy=accuracy,
        )

    def test_get_users_list_by_statistics_ordering_by_attempts_amount(self):
        user = baker.make(User, statistics=None, profile=None)
        user_two = baker.make(User, statistics=None, profile=None)
        self.set_user_statistic(user, 5, 0, 0)
        self.set_user_statistic(user_two, 2, 0, 0)
        users = get_users_list_by_statistics()
        assert user == users[0]
        assert user_two == users[1]

    def test_get_users_list_by_statistics_ordering_by_all_parameters(self):
        user = baker.make(User, statistics=None, profile=None)
        user_two = baker.make(User, statistics=None, profile=None)
        self.set_user_statistic(user, 1, 2, 5)
        self.set_user_statistic(user_two, 1, 5, 2)
        users = get_users_list_by_statistics()
        assert user_two == users[0]
        assert user == users[1]

    def test_get_users_list_by_statistics_return_empty_query_set(self):
        assert not get_users_list_by_statistics().exists()
