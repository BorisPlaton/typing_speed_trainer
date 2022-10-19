from django.db.models import F

from trainer.models import Statistic
from type_results.results_handlers import CurrentUserResults, AllUserResults
from type_results.structs import UserTypingResult


def update_and_cache_user_typing_result(user_id: int, typing_result: UserTypingResult):
    """Updates a user's typing statistic and caches data about it."""
    update_user_statistics(user_id, typing_result.wpm, typing_result.typingAccuracy)
    cache_user_typing_result(user_id, typing_result)


def cache_user_typing_result(user_id: int, typing_result: UserTypingResult):
    """Caches a user's result."""
    user_results = CurrentUserResults(user_id)
    result_id = user_results.add_user_result(typing_result)
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
    return user_cache_results.get_all_user_results()


def update_user_statistics(user_id: int, wpm: int, typing_accuracy: float):
    """Update a user's typing statistic."""
    user_statistics: Statistic = Statistic.objects.get(user__pk=user_id)
    user_statistics.wpm = calculate_average_value_with(user_statistics, 'wpm', wpm)
    user_statistics.accuracy = round(
        calculate_average_value_with(user_statistics, 'accuracy', typing_accuracy), 2
    )
    user_statistics.attempts_amount = F('attempts_amount') + 1
    user_statistics.save()


def calculate_average_value_with(statistics_model: Statistic, field_name: str, value: float) -> float:
    """Calculates a new average value of some `Statistic` model field."""
    current_field_value = getattr(statistics_model, field_name)
    new_field_value = (
            (current_field_value * statistics_model.attempts_amount + value) /
            (statistics_model.attempts_amount + 1)
    )
    return new_field_value
