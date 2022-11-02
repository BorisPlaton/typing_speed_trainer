from dataclasses import dataclass

from account.models import User
from trainer.selectors import get_users_with_ids
from type_results.services import get_last_cached_results_with_users_ids
from type_results.structs import UserTypingResult


@dataclass
class TypeResultWithUser(UserTypingResult):
    """
    Adds a new field with user, and changes the type of
    time to the `datetime`.
    """
    user: User


def get_last_cached_results_with_users(amount: int) -> list[TypeResultWithUser]:
    """
    Returns a list with last cached results. Attaches their
    users and convert date from string to the `datetime` object.
    """
    last_cached_results = get_last_cached_results_with_users_ids()[:amount]
    users_which_allow_show_results = get_users_with_ids([result.user_id for result in last_cached_results]).filter(
        profile__are_results_shown=True
    )
    type_results_with_models = []
    for result in last_cached_results:
        result_values = vars(result)
        user = users_which_allow_show_results.filter(pk=result_values.pop('user_id'))
        if user.exists():
            type_results_with_models.append(
                TypeResultWithUser(**result_values, user=user.first())
            )
    return type_results_with_models[::-1]


def sort_results_by_time(cached_results: list[UserTypingResult]) -> list[UserTypingResult]:
    """Sorts given cached results by their time adding."""
    return sorted(cached_results, key=lambda result: result.dateEnd, reverse=True)
