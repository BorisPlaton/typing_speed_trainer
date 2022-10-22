from django.core.cache import caches


class BaseCacheRepository:
    """
    The base class. It has the instance of cache which is
    used to perform CRUD operations.
    """

    def __init__(self, cache_db_name: str = 'default'):
        """Saves a cache instance which matches a given name."""
        self.cache_db = caches[cache_db_name]
