from collections import deque

from type_results.structs import TypingResultWithUserID


def test_add_result_to_observed_caches_result(all_users_results, user_id, result_id):
    assert not all_users_results.cache_db.get(all_users_results.last_cached_results)
    all_users_results.add_user_result_to_observed(user_id, result_id)
    assert all_users_results.cache_db.get(all_users_results.last_cached_results)


def test_adding_already_existed_result_will_not_affect_cache(all_users_results, user_id, result_id):
    assert not all_users_results.cache_db.get(all_users_results.last_cached_results)
    all_users_results.add_user_result_to_observed(user_id, result_id)
    cached_results_data = all_users_results.cache_db.get(all_users_results.last_cached_results)
    all_users_results.add_user_result_to_observed(user_id, result_id)
    assert cached_results_data == all_users_results.cache_db.get(all_users_results.last_cached_results)


def test_protected_get_last_cached_results_returns_deque_if_cache_is_empty(all_users_results, settings):
    cached_deque = all_users_results._get_last_cached_results_deque()
    assert isinstance(cached_deque, deque)
    assert cached_deque.maxlen == settings.MAX_LENGTH_LAST_CACHED_DEQUE


def test_protected_get_last_cached_results_returns_deque_if_cache_has_values(
        all_users_results, settings, user_id, result_id
):
    all_users_results.add_user_result_to_observed(user_id, result_id)
    cached_deque = all_users_results._get_last_cached_results_deque()
    assert isinstance(cached_deque, deque)
    assert cached_deque.maxlen == settings.MAX_LENGTH_LAST_CACHED_DEQUE
    assert len(cached_deque) == 1


def test_get_cached_results_with_users_ids_returns_empty_list_if_cache_doesnt_have_data(all_users_results):
    assert all_users_results.get_cached_results_with_users_ids() == []


def test_get_cached_results_with_users_ids_returns_typing_results_with_users_ids(
        all_users_results, user_cached_results, generate_user_statistics
):
    users_results_with_ids = []
    for i in range(3):
        user_cached_results.user_id = i
        for j in range(2):
            generated_stats = generate_user_statistics()
            result_id = user_cached_results.add_result(generated_stats)
            all_users_results.add_user_result_to_observed(i, result_id)
            users_results_with_ids.append(TypingResultWithUserID(**vars(generated_stats), user_id=i))
    users_results_from_cache = all_users_results.get_cached_results_with_users_ids()
    for result_from_cache in users_results_from_cache:
        assert result_from_cache in users_results_with_ids
