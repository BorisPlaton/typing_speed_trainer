from dataclasses import dataclass

from account.models import User
from type_results.services import get_last_cached_results_with_users_ids
from type_results.structs import UserTypingResult


@dataclass
class TypeResultWithUser(UserTypingResult):
    user: User


def get_last_cached_results_with_users(amount: int) -> list[TypeResultWithUser]:
    last_cached_results = get_last_cached_results_with_users_ids()[:amount]
    users_models = User.objects.filter(pk__in=[result.user_id for result in last_cached_results])
    type_results_with_user_model = []
    for result in last_cached_results:
        result_values = vars(result)
        user_id = result_values.pop('user_id')
        type_results_with_user_model.append(
            TypeResultWithUser(**result_values, user=users_models.get(pk=user_id))
        )
    return type_results_with_user_model
