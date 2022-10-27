import random

import pytest

from type_results.results_repositories.all_users_results import AllUserResults
from type_results.results_repositories.user_cached_results import UserCachedResults
from type_results.structs import UserTypingResult


@pytest.fixture
def result_id():
    return 2


@pytest.fixture
def expiration_time(settings) -> int:
    return settings.CACHES['default']['TIMEOUT']


@pytest.fixture
def user_id():
    return 1


@pytest.fixture
def user_cached_results(user_id):
    handler = UserCachedResults(user_id)
    yield handler
    handler.cache_db.clear()


@pytest.fixture
def all_users_results():
    handler = AllUserResults()
    yield handler
    handler.cache_db.clear()


@pytest.fixture
def user_statistics_dict():
    return {
        'invalidKeystrokes': random.randint(5, 55),
        'correctKeystrokes': random.randint(5, 55),
        'summaryKeystrokes': random.randint(5, 55),
        'invalidWordsAmount': random.randint(5, 55),
        'correctWordsAmount': random.randint(5, 55),
        'totalWordsAmount': random.randint(5, 55),
        'typingAccuracy': random.randint(5, 55) + 0.1,
        'wpm': random.randint(5, 55),
        'dateEnd': '2022-07-03T16:07:32.225Z',
        'language': 'English',
    }


@pytest.fixture
def generate_user_statistics(user_statistics_dict):
    return lambda: UserTypingResult(**user_statistics_dict)


@pytest.fixture
def user_statistics(generate_user_statistics):
    return generate_user_statistics()
