import pytest

from type_results.results_repositories.key_field import KeyField
from type_results.structs import UserTypingResult


class TestKeyField:

    @pytest.fixture
    def field_name(self):
        return 'field_name'

    @pytest.fixture
    def key_field(self, field_name):
        return KeyField(field_name)

    @pytest.mark.parametrize(
        'regular_string',
        ['1', '', 'some_string']
    )
    def test_key_field_is_equal_to_regular_string(self, regular_string):
        assert KeyField(regular_string) == regular_string

    @pytest.mark.parametrize(
        'additional_args',
        [
            (1, 2, 3),
            ('', 'str', 1)
        ]
    )
    def test_key_field_calling_with_args(self, key_field, additional_args):
        assert key_field(*additional_args) == f'{key_field}:{":".join(map(str, additional_args))}'

    def test_key_field_calling_without_args(self, key_field):
        assert key_field() == key_field


class TestUserTypingResult:

    def test_instance_created_if_passed_data_is_correct(self, user_statistics_dict):
        assert isinstance(UserTypingResult(**user_statistics_dict), UserTypingResult)
