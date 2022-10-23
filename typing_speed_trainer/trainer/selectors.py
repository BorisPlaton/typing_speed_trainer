from django.db.models import QuerySet

from account.models import User


def get_users_with_ids(ids_list: list[int]) -> QuerySet[User]:
    """Returns all users that matches gives ids."""
    return User.objects.filter(pk__in=ids_list)
