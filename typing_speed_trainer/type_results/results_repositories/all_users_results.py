from collections import deque

from django.conf import settings

from type_results.results_repositories.base_repos import BaseCacheRepository
from type_results.results_repositories.key_field import KeyField
from type_results.results_repositories.user_cached_results import UserCachedResults
from type_results.structs import LastUserCachedResults, TypingResultWithUserID


class AllUserResults(BaseCacheRepository):
    """
    Class for retrieving all results from cache, not only a
    specific user results. Max amount records that can be stored
    is defined by variable `MAX_LENGTH_LAST_CACHED_DEQUE` in the
    settings file.
    """

    last_cached_results = KeyField('last_cached_results')

    def add_user_result_to_observed(self, user_id: int, result_id: int):
        """Saves a last cached user result."""
        last_cached_results = self._get_last_cached_results_deque()
        result_data = LastUserCachedResults(user_id=user_id, result_id=result_id)
        if result_data in last_cached_results:
            return
        last_cached_results.appendleft(result_data)
        self.cache_db.set(self.last_cached_results, last_cached_results)

    def get_cached_results_with_users_ids(self) -> list[TypingResultWithUserID | None]:
        """
        Returns last cached results with users ids. If none, returns
        an empty list.
        """
        last_results_data = []
        if not (results_from_cache := self._get_last_cached_results_deque()):
            return last_results_data

        users_results_ids: [int, list[int]] = {}
        for cached_result in results_from_cache:
            if not users_results_ids.get(cached_result.user_id):
                users_results_ids[cached_result.user_id] = []
            users_results_ids[cached_result.user_id].append(cached_result.result_id)

        for user_id, results_ids in users_results_ids.items():
            last_results_data += [
                TypingResultWithUserID(**vars(result), user_id=user_id) for result in
                UserCachedResults(user_id).get_all_results(results_ids)
            ]

        return last_results_data

    def _get_last_cached_results_deque(self) -> deque[LastUserCachedResults | None]:
        """
        Returns a queue with `LastUserCachedResults` instances. If none,
        returns an empty queue with fixed length.
        """
        return self.cache_db.get(
            self.last_cached_results,
            deque(maxlen=settings.MAX_LENGTH_LAST_CACHED_DEQUE)
        )
