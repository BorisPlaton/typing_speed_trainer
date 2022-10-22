import copy

import pytest

from type_results.structs import UserTypingResult


def test_added_user_result_is_stored_in_cache(user_results_handler, user_statistics):
    result_id = user_results_handler.add_result(user_statistics)
    user_data = user_results_handler.get_result_by_id(result_id)
    assert user_data == user_statistics
    assert isinstance(user_data, UserTypingResult)


def test_get_non_existed_result_returns_none(user_results_handler):
    assert user_results_handler.get_result_by_id(-1) is None


@pytest.mark.parametrize(
    'wrong_value',
    [
        1, '', dict, 1.0, {1, 2}, {}
    ]
)
def test_adding_value_with_invalid_type_will_cause_an_exception(user_results_handler, wrong_value):
    with pytest.raises(ValueError):
        user_results_handler.add_result(wrong_value)


def test_access_all_user_results_returns_list_with_data(user_results_handler, user_statistics):
    results_amount = 3
    for _ in range(results_amount):
        user_results_handler.add_result(user_statistics)
    all_user_results = user_results_handler.get_all_results()
    assert len(all_user_results) == results_amount
    for result in all_user_results:
        assert result == user_statistics


def test_get_all_user_results_returns_list_with_results_as_they_were_added(user_results_handler):
    fake_results = ['1', '2', '3']
    for fake_result in fake_results:
        user_results_handler.cache_handler.add_result(fake_result, user_results_handler.user_id)
    all_user_results = user_results_handler.get_all_results()
    for result, fake_result in zip(all_user_results, fake_results):
        assert result == fake_result


def test_current_result_id_is_correct(user_results_handler, user_statistics):
    result_id = None
    assert result_id == user_results_handler._current_result_id
    for _ in range(5):
        result_id = user_results_handler.add_result(user_statistics)
    assert result_id == user_results_handler._current_result_id


def test_delete_all_user_result_clean_cache(user_results_handler, user_statistics):
    user_results_handler.add_result(user_statistics)
    assert user_results_handler._current_result_id
    assert user_results_handler.get_all_results()
    user_results_handler.delete_all_self_results()
    assert user_results_handler._current_result_id is None
    assert user_results_handler.get_all_results() == []


def test_delete_all_user_results_affect_only_specific_user(user_results_handler, user_statistics):
    second_user_results_handler = copy.copy(user_results_handler)
    second_user_results_handler.user_id = user_results_handler.user_id + 1

    user_results_handler.add_result(user_statistics)
    assert user_results_handler._current_result_id
    assert user_results_handler.get_all_results()

    assert second_user_results_handler._current_result_id is None
    assert second_user_results_handler.get_all_results() == []
    second_user_results_handler.add_result(user_statistics)

    user_results_handler.delete_all_self_results()

    assert second_user_results_handler._current_result_id
    assert second_user_results_handler.get_all_results()
