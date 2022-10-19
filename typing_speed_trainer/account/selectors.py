from django.db.models import QuerySet

from account.models import User


def get_users_list_by_statistics() -> QuerySet[User]:
    """Возвращает отсортированные данные о статистике пользователя."""
    queryset = get_user_with_profile().select_related('statistics').order_by(
        '-statistics__attempts_amount',
        '-statistics__wpm',
        '-statistics__accuracy'
    )
    return queryset


def get_user_with_profile(user_id: int = None) -> QuerySet[User]:
    """
    Возвращает QuerySet пользователей с моделей профилей. Если указан
    `id`пользователя, вернет только его модель.
    """
    user_queryset = User.objects.select_related('profile')
    if user_id:
        user_queryset.filter(pk=user_id)
    return user_queryset
