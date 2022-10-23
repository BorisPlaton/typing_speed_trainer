from dataclasses import dataclass
from typing import NamedTuple


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
        """Invokes the validation of values types."""
        self._validate_types()

    def _validate_types(self):
        """Ensures that all values have appropriate types."""
        for field_name, field_type in self.__annotations__.items():
            field_value = getattr(self, field_name)
            if not isinstance(field_value, field_type):
                raise ValueError(
                    "`{}` is not a `{}` type. It is actually a `{}`".format(
                        field_name, field_type, type(field_value)
                    ))


@dataclass
class TypingResultWithUserID(UserTypingResult):
    """
    Has an additional field `user` which contains the owner
    of result.
    """
    user_id: int
