import pytest

from type_results.results_repositories.user_cached_results import ResultCacheHandler
from type_results.results_repositories.results_handlers import CurrentUserResults
from type_results.structs import UserTypingResult


@pytest.fixture
def cache_handler():
    handler = ResultCacheHandler('default')
    yield handler
    handler.clean_cache()


@pytest.fixture
def user_id():
    return 1


@pytest.fixture
def user_results_handler(cache_handler, user_id):
    handler = CurrentUserResults(user_id)
    handler.cache_handler = cache_handler
    return handler


@pytest.fixture
def expiration_time(settings) -> int:
    return settings.CACHES['default']['TIMEOUT']


@pytest.fixture
def user_statistics():
    return UserTypingResult(**{
        'invalidKeystrokes': 55,
        'correctKeystrokes': 55,
        'summaryKeystrokes': 55,
        'invalidWordsAmount': 55,
        'correctWordsAmount': 55,
        'totalWordsAmount': 55,
        'typingAccuracy': 88.2,
        'wpm': 40,
        'dateEnd': '2022-07-03T16:07:32.225Z',
    })
