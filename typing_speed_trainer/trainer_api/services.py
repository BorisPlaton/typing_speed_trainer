from django.db.models import F, QuerySet

from trainer.models import Statistic
from type_results.services import cache_user_typing_result
from type_results.structs import UserTypingResult


def update_and_cache_user_typing_result(user_id: int, typing_result: UserTypingResult):
    """Updates a user's typing statistic and caches data about it."""
    update_user_statistics(user_id, typing_result.wpm, typing_result.typingAccuracy)
    cache_user_typing_result(user_id, typing_result)


def update_user_statistics(user_id: int, wpm: int, typing_accuracy: float):
    """Update a user's typing statistic."""
    user_statistics: QuerySet[Statistic] = Statistic.objects.filter(
        user__pk=user_id, user__profile__are_results_shown=True
    )
    if not user_statistics.exists():
        return
    user_statistics: Statistic = user_statistics.first()
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
