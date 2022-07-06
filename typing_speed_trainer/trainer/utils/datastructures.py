from datetime import datetime
from typing import TypedDict, NamedTuple

from account.models import User


class LastUserCachedResults(NamedTuple):
    """
    Последний результат пользователя, что был сохранён
    в кэше.
    """
    user_id: int
    result_id: int


class UserTypingResult(TypedDict):
    """
    Результат пользователя по тренажеру, что получается с
    помощью AJAX-запроса после чего кэшируется.
    """
    invalidKeystrokes: int
    correctKeystrokes: int
    summaryKeystrokes: int
    invalidWordsAmount: int
    correctWordsAmount: int
    totalWordsAmount: int
    typingAccuracy: float | int
    wpm: int
    dateEnd: datetime | str


class UserTypingResultWithUser(UserTypingResult):
    """
    То же самое, что и в `UserTypingResult`, но имеет модель
    `User` по ключу `user`.
    """
    user: User


class ResultFieldType(NamedTuple):
    """Название и тип поля статистики пользователя."""
    field_name: str
    field_type: type(int | float) | type(str) | type(datetime)
