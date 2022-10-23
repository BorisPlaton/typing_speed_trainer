from dataclasses import dataclass
from datetime import datetime

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
    dateEnd: datetime


def get_last_cached_results_with_users(amount: int) -> list[TypeResultWithUser]:
    """
    Returns a list with last cached results. Attaches their
    users and convert date from string to the `datetime` object.
    """
    last_cached_results = get_last_cached_results_with_users_ids()[:amount]
    users_models = get_users_with_ids([result.user_id for result in last_cached_results])
    type_results_with_user_model = []
    for result in last_cached_results:
        result_values = vars(result)
        user = users_models.get(pk=result_values.pop('user_id'))
        datetime_object = make_datetime_from_string(result_values.pop('dateEnd'))
        type_results_with_user_model.append(
            TypeResultWithUser(**result_values, user=user, dateEnd=datetime_object)
        )
    return type_results_with_user_model[::-1]


def make_datetime_from_string(date_in_string: str, date_format: str = '%Y-%m-%dT%H:%M:%S.%fZ') -> datetime:
    """Converts date from string to the datetime object."""
    return datetime.strptime(date_in_string, date_format)
