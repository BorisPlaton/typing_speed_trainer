from django.core.cache import caches
from django_redis.cache import RedisCache


class ResultCacheHandler:
    """
    The class is aimed at interaction with a cache to perform
    CRUD operations with user's type trainer results.
    """

    def get_result(self, result_id: int, user_id: int):
        """Returns the type results from cache of specific user."""
        return self.cache_db.get(f'result:{result_id}', version=user_id)

    def add_result(self, data, user_id: int) -> int:
        """Adds a result to the cache. The result's id is returned."""
        result_id = self.increment_current_result_id(user_id)
        self.cache_db.set(f'result:{result_id}', data, version=user_id)
        return result_id

    def delete_result(self, result_id: int, user_id: int) -> bool:
        """Deletes a result from the cache."""
        return self.cache_db.delete(f'result:{result_id}', version=user_id)

    def set_current_result_id(self, new_result_id: int, user_id: int):
        """Sets a last result id. It can't be less than zero."""
        if new_result_id <= 0:
            raise ValueError("`new_result_id` не может быть меньше нуля.")
        self.cache_db.set('last_result_id', new_result_id, version=user_id)

    def get_current_result_id(self, user_id: int):
        """Returns the last result id of specific user."""
        return self.cache_db.get('last_result_id', version=user_id)

    def delete_current_result_id(self, user_id: int):
        """Deletes a current result id."""
        self.cache_db.delete('last_result_id', version=user_id)

    def increment_current_result_id(self, user_id: int) -> int:
        """
        Increments a current result id. If the id doesn't exist, it
        will create it.
        """
        if self.get_current_result_id(user_id) is None:
            self.set_current_result_id(1, user_id)
            return 1
        else:
            return self.cache_db.incr('last_result_id', version=user_id)

    def get_results_keynames(self, user_id: int) -> list[str | None]:
        """Returns all keys of results from cache if they exist."""
        if (current_id := self.get_current_result_id(user_id)) is None:
            return []
        result_key_names = []
        for result_id in range(current_id, 0, -1):
            if self.get_result(result_id, user_id) is None:
                break
            result_key_names.append(f'result:{result_id}')
        return result_key_names

    def clean_cache(self):
        """Deletes ALL values from cache."""
        self.cache_db.clear()

    @property
    def cache_db(self) -> RedisCache:
        """Returns a cache instance that stores all values."""
        return caches[self.cache_db_name]

    def __init__(self, cache_db_name: str = 'default'):
        self.cache_db_name = cache_db_name
