import pytest

from type_results.handlers.cache_handler import ResultCacheHandler


@pytest.fixture
def cache_handler():
    handler = ResultCacheHandler('default')
    yield handler
    handler.clean_cache()


@pytest.fixture
def user_id():
    return 1


@pytest.fixture
def expiration_time(settings) -> int:
    return settings.CACHES['default']['TIMEOUT']
