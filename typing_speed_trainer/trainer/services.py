from account.selectors import get_user_with_profile
from type_results.results_handlers import UserTypingResultWithUser, AllUserResults


def get_last_cached_results_with_users(results_amount: int) -> list[UserTypingResultWithUser]:
    """
    Возвращает определенное количество записей последних результатов
    из кеша с их пользователями.
    """
    user_cache_results = AllUserResults()
    return user_cache_results.get_cached_results_with_users(results_amount, get_user_with_profile())
