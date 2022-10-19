from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple

from account.models import User


class LastUserCachedResults(NamedTuple):
    """The last user result that was saved to the cache."""

    user_id: int
    result_id: int


@dataclass
class UserTypingResult:
    """The user typing results."""

    invalidKeystrokes: int
    correctKeystrokes: int
    summaryKeystrokes: int
    invalidWordsAmount: int
    correctWordsAmount: int
    totalWordsAmount: int
    typingAccuracy: float | int
    wpm: int
    dateEnd: str

    def __post_init__(self):
        """Invokes the validation of values types and the time format."""
        self._validate_initialized_data()

    def _validate_initialized_data(self):
        self._validate_types()
        self._validate_time_format(self.dateEnd, '%Y-%m-%dT%H:%M:%S.%fZ')

    def _validate_types(self):
        for field_name, field_type in self.__annotations__.items():
            field_value = getattr(self, field_name)
            if not isinstance(field_value, field_type):
                raise ValueError(
                    "`{}` is not a `{}` type. It is actually a `{}`".format(
                        field_name, field_type, type(field_value)
                    ))

    @staticmethod
    def _validate_time_format(to_validate_time: str, time_format: str):
        datetime.strptime(to_validate_time, time_format)


@dataclass
class UserTypingResultWithUser(UserTypingResult):
    """
    Has an additional field `user` which contains the owner of result.
    """

    user: User
