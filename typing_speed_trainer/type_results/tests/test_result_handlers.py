import copy
import time

import pytest

from type_results.structs import UserTypingResult


def test_added_user_result_is_stored_in_cache(user_cached_results, user_statistics):
    result_id = user_cached_results.add_result(user_statistics)
    user_data = user_cached_results.get_result(result_id)
    assert user_data == user_statistics
    assert isinstance(user_data, UserTypingResult)


def test_only_positive_integer_can_be_result_id(user_cached_results):
    with pytest.raises(ValueError):
        user_cached_results._current_result_id = 0


def test_if_result_id_doesnt_exist_increment_will_create_it(user_cached_results, ):
    assert user_cached_results._current_result_id is None
    user_cached_results._increment_current_result_id()
    assert user_cached_results._current_result_id == 1


def test_get_result_keynames_returns_all_keynames_from_cache(user_cached_results):
    results_amount = 5
    for i in range(results_amount):
        user_cached_results.add_result({})
    assert len(user_cached_results._get_results_keynames()) == results_amount


def test_get_result_keynames_returns_empty_list_if_result_id_doesnt_exist(user_cached_results):
    assert user_cached_results._get_results_keynames() == []


def test_get_result_keynames_returns_all_keynames_from_cache_that_have_not_expired(
        user_cached_results, expiration_time
):
    for _ in range(5):
        user_cached_results.add_result({})
    time.sleep(expiration_time)
    existed_data = {'one': 1}
    user_cached_results.add_result(existed_data)
    keynames = user_cached_results._get_results_keynames()
    assert len(keynames) == 1
    assert user_cached_results.cache_db.get(keynames[0], version=user_cached_results.user_id) == existed_data


def test_get_non_existed_result_returns_none(user_cached_results):
    assert user_cached_results.get_result(-1) is None


def test_add_user_result_to_cache_will_return_incremented_result_id(user_cached_results):
    assert user_cached_results.add_result({}) == 1
    assert user_cached_results.add_result({}) == 2
    assert user_cached_results.add_result({}) == 3


def test_results_in_cache_expires_during_some_time(expiration_time, user_cached_results):
    data = {}
    result_id = user_cached_results.add_result(data)
    assert user_cached_results.get_result(result_id) == data
    time.sleep(expiration_time)
    assert user_cached_results.get_result(result_id) is None
    assert user_cached_results._current_result_id


def test_access_all_user_results_returns_list_with_data(user_cached_results, user_statistics):
    results_amount = 3
    for _ in range(results_amount):
        user_cached_results.add_result(user_statistics)
    all_user_results = user_cached_results.get_all_results()
    assert len(all_user_results) == results_amount
    for result in all_user_results:
        assert result == user_statistics


def test_get_all_user_results_returns_list_with_results_as_they_were_added(user_cached_results):
    fake_results = ['1', '2', '3']
    for fake_result in fake_results:
        user_cached_results.add_result(fake_result)
    all_user_results = user_cached_results.get_all_results()
    for result, fake_result in zip(all_user_results, fake_results):
        assert result == fake_result


def test_get_all_results_with_specific_ids(user_cached_results):
    fake_results = [1, 2, 3]
    fake_results_ids = [user_cached_results.add_result(result) for result in fake_results]
    all_user_results = user_cached_results.get_all_results(fake_results_ids[1:])
    assert all_user_results[0] == fake_results[1]
    assert all_user_results[1] == fake_results[2]


def test_get_all_results_with_not_existed_ids_returns_empty_list(user_cached_results):
    assert user_cached_results.get_all_results([100, 200, 301]) == []


def test_current_result_id_is_correct(user_cached_results, user_statistics):
    result_id = None
    assert result_id == user_cached_results._current_result_id
    for _ in range(5):
        result_id = user_cached_results.add_result(user_statistics)
    assert result_id == user_cached_results._current_result_id


def test_delete_all_user_result_clean_cache(user_cached_results, user_statistics):
    user_cached_results.add_result(user_statistics)
    assert user_cached_results._current_result_id
    assert user_cached_results.get_all_results()
    user_cached_results.delete_all_self_results()
    assert user_cached_results.get_all_results() == []


def test_delete_all_user_results_affect_only_specific_user(user_cached_results, user_statistics):
    second_user_results_handler = copy.copy(user_cached_results)
    second_user_results_handler.user_id = user_cached_results.user_id + 1

    user_cached_results.add_result(user_statistics)
    assert user_cached_results._current_result_id
    assert user_cached_results.get_all_results()

    assert second_user_results_handler.get_all_results() == []
    second_user_results_handler.add_result(user_statistics)

    user_cached_results.delete_all_self_results()

    assert second_user_results_handler._current_result_id
    assert second_user_results_handler.get_all_results()
