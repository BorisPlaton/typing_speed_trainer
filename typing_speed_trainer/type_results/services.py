from account.selectors import get_user_with_profile

from type_results.results_repositories.results_handlers import CurrentUserResults, AllUserResults
from type_results.structs import TypingResultWithUserID, UserTypingResult


def get_last_cached_results_with_users(results_amount: int) -> list[TypingResultWithUserID]:
    """
    Returns the specified amount of last cached results with
    their users.
    """
    user_cache_results = AllUserResults()
    return user_cache_results.get_cached_results_with_users_ids(results_amount, get_user_with_profile())


def cache_user_typing_result(user_id: int, typing_result: UserTypingResult):
    """Caches a user's result."""
    user_results = CurrentUserResults(user_id)
    result_id = user_results.add_result(typing_result)
    add_user_result_to_observed(user_id, result_id)


def add_user_result_to_observed(user_id: int, result_id: int):
    """
    Adds a result's id and a user's id to the observed in a cache. It
    helps in future fetch result data with its owner - the user.
    """
    all_results = AllUserResults()
    all_results.add_to_cached_results(user_id, result_id)


def get_all_user_results(user_id: int):
    """Returns all results data that are present in the cache."""
    user_cache_results = CurrentUserResults(user_id)
    return user_cache_results.get_all_results()


def delete_all_user_cached_results(user_id: int):
    """Deletes all user's cached results."""
    cache = CurrentUserResults(user_id)
    cache.delete_all_self_results()
