from django.test import TestCase
from parameterized import parameterized

from trainer.utils.cache_results import ResultCache, CurrentUserCache


class TestResultCache(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = {
            'first': 1,
            'second': 2,
            'third': 3,
        }

    def setUp(self) -> None:
        self.cache = ResultCache()
        self.cache.cache_base_name = 'test'

    def tearDown(self) -> None:
        self.cache.result_cache.clear()

    def test_cache_base_name_is_necessarily(self):
        some_cache = ResultCache()
        some_cache.cache_base_name = ''
        self.assertRaises(ValueError, lambda: some_cache.result_cache)

    @parameterized.expand([
        (('string',),),
        (12,),
        ({'s': 1},),
        ("",),
        (set(),),
        (1.,),
    ])
    def test_cache_base_name_accepts_only_str_type(self, wrong_cache_base_type):
        some_cache = ResultCache()
        some_cache.cache_base_name = wrong_cache_base_type
        self.assertRaises(ValueError, lambda: some_cache.result_cache)

    @parameterized.expand([
        (1, 2),
        (-1, 4),
    ])
    def test_get_user_result_without_cache_data(self, result_id, user_id):
        self.assertIsNone(self.cache.get_user_result(result_id, user_id))

    @parameterized.expand([
        (1., 2),
        (set(), '2'),
        (tuple(), 5),
        (frozenset(), int),
        (list(), .2),
        (dict(), {1: 2, 2: 3}),
    ])
    def test_get_user_result_raise_error_with_invalid_input_data(self, result_id, user_id):
        self.assertRaises(ValueError, lambda: self.cache.get_user_result(result_id, user_id))

    def test_set_user_result(self):
        for i in range(6):
            self.cache.set_user_result(i, i)
        for i in range(6):
            self.assertEqual(
                self.cache.get_user_result(self.cache.get_user_current_result_id(i), i),
                i,
            )

    @parameterized.expand([
        ('fafa', set()),
        ({}, '2'),
        (22., 5.),
        (3, int),
        (5, .2),
        (set(), {1: 2, 2: 3}),
    ])
    def test_set_user_result_raise_error_with_invalid_input_data(self, data, user_id):
        self.assertRaises(ValueError, lambda: self.cache.set_user_result(data, user_id))

    def test_delete_user_result(self):
        self.cache.set_user_result(self.data, 2)
        self.assertTrue(self.cache.delete_user_result(1, 2))
        self.assertFalse(self.cache.delete_user_result(55, 4))

    @parameterized.expand([
        (1,),
        (22,),
        (4,),
        (5,),
    ])
    def test_get_user_current_result_id_without_cache_data(self, user_id):
        self.assertFalse(
            self.cache.get_user_current_result_id(user_id)
        )

    @parameterized.expand([
        (12,),
        (1,),
        (-55,),
        (0,),
    ])
    def test_get_user_current_result_id_without_cache_data(self, user_id):
        self.assertFalse(
            self.cache.get_user_current_result_id(user_id)
        )

    @parameterized.expand([
        (15, -1),
        (1, -11),
        (16, 2),
        (1, 5),
        (2, 0),
    ])
    def test_set_user_current_result_id(self, new_result_id, user_id):
        try:
            self.cache._set_user_current_result_id(new_result_id, user_id)
        except ValueError:
            self.assertIsNone(self.cache.get_user_current_result_id(user_id))
        else:
            self.assertEqual(self.cache.get_user_current_result_id(user_id), new_result_id)

    def test_increment_current_result_id(self):
        self.cache._set_user_current_result_id(2, 1)
        self.assertEqual(self.cache.increment_current_result_id(1), 3)
        self.assertEqual(self.cache.increment_current_result_id(2), 1)

    def test_get_results_keynames(self):
        for i in range(5):
            self.cache.set_user_result(self.data, 1)

        for num in range(1, 5):
            self.assertTrue(f'result:{num}' in self.cache.get_results_keynames(1))

    def test_one_data_but_different_user_id(self):
        self.cache.set_user_result({'first data': 2}, 1)
        self.cache.set_user_result({'second data'}, 2)
        self.assertNotEqual(
            self.cache.get_user_result(1, 1),
            self.cache.get_user_result(1, 2)
        )


class TestCurrentUserCache(TestCase):

    def setUp(self) -> None:
        self.current_user_cache = CurrentUserCache()
        self.current_user_cache.cache_base_name = 'test'
        self.current_user_cache.user_id = 1
        self.result_data = {
            'invalidKeystrokes': 55,
            'correctKeystrokes': 55,
            'summaryKeystrokes': 55,
            'invalidWordsAmount': 55,
            'correctWordsAmount': 55,
            'totalWordsAmount': 55,
            'typingAccuracy': 88.2,
            'wpm': 40,
            'dateEnd': '2022-07-03T16:07:32.225Z',
        }

    def tearDown(self) -> None:
        self.current_user_cache.result_cache.clear()

    def test_current_user_result_id(self):
        for i in range(5):
            self.current_user_cache._set_user_current_result_id(i, i)

        self.assertEqual(
            self.current_user_cache.current_user_result_id, self.current_user_cache.user_id
        )

    def test_difference_between_different_users_using_current_user_result_id(self):
        self.current_user_cache.increment_current_user_result_id()
        first_user_result_id = self.current_user_cache.current_user_result_id

        self.current_user_cache.user_id = 2
        self.current_user_cache._set_user_current_result_id(4, 2)
        second_user_result_id = self.current_user_cache.current_user_result_id

        self.assertNotEqual(
            first_user_result_id, second_user_result_id
        )

    def test_get_all_current_user_results_gives_correct_results_list(self):
        user_data = [
            ['tre', 2],
            1,
            '1',
            'two',
        ]
        for data in user_data:
            self.current_user_cache.set_current_user_result(data)
        self.assertTrue(self.current_user_cache.get_all_current_user_results())

        self.current_user_cache.user_id = 2
        self.assertFalse(self.current_user_cache.get_all_current_user_results())

        self.current_user_cache.user_id = 1

        for data in user_data:
            self.assertTrue(data in self.current_user_cache.get_all_current_user_results())
