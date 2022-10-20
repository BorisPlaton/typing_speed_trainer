from account.models import User, Profile
from trainer.models import Statistic


def create_user_statistic(user: User):
    """Creates a new `Statistic` record of a given user."""
    Statistic.objects.create(user=user)


def create_user_profile(user: User):
    """Creates a new `Profile` record of a given user."""
    Profile.objects.create(user=user)
