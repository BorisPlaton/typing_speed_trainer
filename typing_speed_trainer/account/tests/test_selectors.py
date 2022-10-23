from account.models import User
from account.selectors import get_users_list_by_statistics
from tests.utils import BaseTestCase
from trainer.models import Statistic


class TestServicesModelsUtils(BaseTestCase):

    @staticmethod
    def set_user_statistic(user: User, attempts_amount, wpm, accuracy):
        Statistic.objects.filter(pk=user.statistics.pk).update(
            attempts_amount=attempts_amount,
            wpm=wpm,
            accuracy=accuracy,
        )

    def test_get_users_list_by_statistics_ordering_by_attempts_amount(self, user, second_user):
        self.set_user_statistic(user, 5, 0, 0)
        self.set_user_statistic(second_user, 2, 0, 0)
        users = get_users_list_by_statistics()
        assert user == users[0]
        assert second_user == users[1]

    def test_get_users_list_by_statistics_ordering_by_all_parameters(self, user, second_user):
        self.set_user_statistic(user, 1, 2, 5)
        self.set_user_statistic(second_user, 1, 5, 2)
        users = get_users_list_by_statistics()
        assert second_user == users[0]
        assert user == users[1]

    def test_get_users_list_by_statistics_return_empty_query_set(self):
        assert not get_users_list_by_statistics().exists()
