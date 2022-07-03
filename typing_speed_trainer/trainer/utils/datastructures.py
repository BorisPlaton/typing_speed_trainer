from datetime import datetime
from typing import TypedDict, NamedTuple


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


class ResultFieldType(NamedTuple):
    """Название и тип поля статистики пользователя."""
    field_name: str
    field_type: type(int | float) | type(str) | type(datetime)
