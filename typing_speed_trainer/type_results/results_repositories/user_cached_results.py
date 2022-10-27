from type_results.results_repositories.base_repos import BaseCacheRepository
from type_results.results_repositories.key_field import KeyField
from type_results.structs import UserTypingResult


class UserCachedResults(BaseCacheRepository):
    """
    The class is aimed at interaction with a cache to perform
    CRUD operations with user's type trainer results.
    """

    type_result = KeyField('result')
    last_result_id = KeyField('current_result_id')

    def get_result(self, result_id: int) -> UserTypingResult:
        """Returns the type results from cache of specific user."""
        return self.cache_db.get(self.type_result(result_id), version=self.user_id)

    def get_all_results(self, results_ids: list[int] = None) -> list[UserTypingResult | None]:
        """
        Returns a list with all user statistics from cache. If none
        exist, returns an empty list.
        """
        results_keys = self._get_results_keynames(results_ids or None)
        results = self.cache_db.get_many(results_keys, version=self.user_id)
        return [result for result in results.values()][::-1]

    def add_result(self, data: UserTypingResult) -> int:
        """Adds a result to the cache. The result's id is returned."""
        result_id = self._increment_current_result_id()
        self.cache_db.set(self.type_result(result_id), data, version=self.user_id)
        return result_id

    def delete_all_self_results(self, results_ids: list[int] = None) -> int:
        """
        Deletes all user results and returns the amount
        of affected records. Also, it can delete only specified
        results which id is in given ids.
        """
        if result_keynames := self._get_results_keynames(results_ids):
            self.cache_db.delete_many(result_keynames, version=self.user_id)
        del self._current_result_id
        return len(result_keynames)

    @property
    def _current_result_id(self):
        """Returns the current result id of current user."""
        return self.cache_db.get(self.last_result_id, version=self.user_id)

    @_current_result_id.setter
    def _current_result_id(self, new_result_id: int):
        """Sets a current result id. It can't be less than zero."""
        if new_result_id <= 0:
            raise ValueError("`new_result_id` can't be less than zero.")
        self.cache_db.set(self.last_result_id, new_result_id, version=self.user_id, timeout=None)

    @_current_result_id.deleter
    def _current_result_id(self):
        """Deletes a current result id."""
        self.cache_db.delete(self.last_result_id, version=self.user_id)

    def _get_results_keynames(self, results_ids: list[int] = None) -> list[str | None]:
        """Returns all keys of results from cache if they exist."""
        if results_ids:
            results_ids = sorted(results_ids, reverse=True)
        elif (current_id := self._current_result_id) is None:
            return []
        else:
            results_ids = range(current_id, 0, -1)

        result_key_names = []
        for result_id in results_ids:
            if self.get_result(result_id) is None:
                continue
            result_key_names.append(self.type_result(result_id))
        return result_key_names

    def _increment_current_result_id(self) -> int:
        """
        Increments a current result id. If the id doesn't exist, it
        will create it.
        """
        if self._current_result_id is None:
            self._current_result_id = 1
            return 1
        else:
            return self.cache_db.incr(self.last_result_id, version=self.user_id)

    def __init__(self, user_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
