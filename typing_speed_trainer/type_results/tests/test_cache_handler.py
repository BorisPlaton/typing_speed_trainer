import time

import pytest


@pytest.mark.parametrize(
    'result_id, user_id_',
    [(1, 2), (-1, 4)]
)
def test_if_no_data_in_cache_get_user_result_returns_none(cache_handler, result_id, user_id_):
    assert cache_handler.get_result(result_id, user_id_) is None


def test_add_user_result_to_cache_will_return_incremented_result_id(cache_handler, user_id):
    assert cache_handler.add_result({}, user_id) == 1
    assert cache_handler.add_result({}, user_id) == 2
    assert cache_handler.add_result({}, user_id) == 3


def test_results_in_cache_expires_during_some_time(expiration_time, cache_handler, user_id):
    data = {}
    result_id = cache_handler.add_result(data, user_id)
    assert cache_handler.get_result(result_id, user_id) == data
    time.sleep(expiration_time)
    assert cache_handler.get_result(result_id, user_id) is None
    assert cache_handler.get_current_result_id(user_id) is None


def test_delete_user_result_will_return_boolean_value(cache_handler, user_id):
    result_id = cache_handler.add_result({}, user_id)
    assert cache_handler.delete_result(result_id, user_id)
    assert not cache_handler.delete_result(result_id, user_id)


def test_result_deletion_will_affect_only_one_record(cache_handler, user_id):
    results_ids = []
    data = {'one': 1, 'two': 2}
    for _ in range(3):
        results_ids.append(cache_handler.add_result(data, user_id))
    assert cache_handler.delete_result(results_ids[0], user_id)
    assert cache_handler.get_result(results_ids[0], user_id) is None
    assert cache_handler.get_result(results_ids[1], user_id) == data
    assert cache_handler.get_result(results_ids[2], user_id) == data


def test_if_user_id_doesnt_exist_current_result_id_is_none(cache_handler):
    assert cache_handler.get_current_result_id(0) is None


@pytest.mark.parametrize(
    'result_id',
    [0, -1, -2]
)
def test_only_positive_integer_can_be_result_id(cache_handler, result_id):
    with pytest.raises(ValueError):
        cache_handler.set_current_result_id(result_id, 0)


def test_if_result_id_doesnt_exist_increment_will_create_it(cache_handler, user_id):
    assert cache_handler.get_current_result_id(user_id) is None
    cache_handler.increment_current_result_id(user_id)
    assert cache_handler.get_current_result_id(user_id) == 1


def test_increment_result_id_increases_it_on_one(cache_handler, user_id):
    result_id = 50
    cache_handler.set_current_result_id(result_id, user_id)
    assert cache_handler.get_current_result_id(user_id)
    cache_handler.increment_current_result_id(user_id)
    assert cache_handler.get_current_result_id(user_id) == result_id + 1


def test_get_result_keynames_returns_all_keynames_from_cache(cache_handler, user_id):
    results_amount = 5
    for i in range(results_amount):
        cache_handler.add_result({}, user_id)
    assert len(cache_handler.get_results_keynames(user_id)) == results_amount


def test_get_result_keynames_returns_empty_list_if_result_id_doesnt_exist(cache_handler, user_id):
    assert cache_handler.get_results_keynames(user_id) == []


def test_get_result_keynames_returns_all_keynames_from_cache_that_have_not_expired(
        cache_handler, user_id, expiration_time
):
    for _ in range(5):
        cache_handler.add_result({}, user_id)
    time.sleep(expiration_time)
    existed_data = {'one': 1}
    cache_handler.add_result(existed_data, user_id)
    keynames = cache_handler.get_results_keynames(user_id)
    assert len(keynames) == 1
    assert cache_handler.cache_db.get(keynames[0], version=user_id) == existed_data


def test_clean_cache_deletes_all_from_cache(cache_handler, user_id):
    result_id = cache_handler.add_result({'one': 1}, user_id)
    assert cache_handler.get_result(result_id, user_id)
    cache_handler.clean_cache()
    assert cache_handler.get_result(result_id, user_id) is None


def test_delete_result_id_will_clean_it_from_cache(cache_handler, user_id):
    cache_handler.set_current_result_id(10, user_id)
    cache_handler.delete_current_result_id(user_id)
    assert cache_handler.get_current_result_id(user_id) is None
    assert cache_handler.increment_current_result_id(user_id) == 1
