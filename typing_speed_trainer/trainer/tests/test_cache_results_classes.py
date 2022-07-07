from django.test import TestCase
from parameterized import parameterized

from trainer.utils.cache_results import ResultCache


class TestResultCache(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = {
            'first': 1,
            'second': 2,
            'third': 3,
        }

    def setUp(self) -> None:
        self.result_cache = ResultCache()
        self.result_cache.cache_base_name = 'test'

    def tearDown(self) -> None:
        self.result_cache.result_cache.clear()

    @parameterized.expand([
        (1, 2),
        (-1, 4),
        ('sss', 2),
        (1, 'ss2'),
        ([], 2),
        ('', ''),
    ])
    def test_get_user_result_without_cache_data(self, result_id, user_id):
        self.assertIsNone(self.result_cache.get_user_result(result_id, user_id))

    @parameterized.expand([
        (1, 2),
        (-1, 4),
        ('sss', 2),
        (1, 'ss2'),
        ([], 2),
        ('', ''),
        ([1, 2, 3, 4], 1),
        (2.0, 1.0),
    ])
    def test_set_user_result(self, result_id, user_id):
        try:
            self.result_cache.set_user_result(result_id, self.data, user_id)
        except ValueError:
            self.assertIsNone(self.result_cache.get_user_result(result_id, user_id))
        else:
            self.assertEqual(self.result_cache.get_user_result(result_id, user_id), self.data)

    def test_delete_user_result(self):
        self.result_cache.set_user_result(1, self.data, 2)
        self.assertTrue(self.result_cache.delete_user_result(1, 2))
        self.assertFalse(self.result_cache.delete_user_result(55, 4))

    @parameterized.expand([
        (1,),
        ('',),
        (1.,),
        (4,),
        (1.0,),
    ])
    def test_get_user_current_result_id_without_cache_data(self, user_id):
        self.assertFalse(
            self.result_cache.get_user_current_result_id(user_id)
        )

    @parameterized.expand([
        (1,),
        ('',),
        (1.,),
        (4,),
        (1.0,),
    ])
    def test_get_user_current_result_id_without_cache_data(self, user_id):
        self.assertFalse(
            self.result_cache.get_user_current_result_id(user_id)
        )

    @parameterized.expand([
        (1, '4'),
        ('', 2),
        (1., 5),
        (4, [4242, ]),
        (set(), dict()),
    ])
    def test_set_user_current_result_id(self, new_result_id, user_id):
        try:
            self.result_cache.set_user_current_result_id(new_result_id, user_id)
        except ValueError:
            self.assertIsNone(self.result_cache.get_user_current_result_id(user_id))
        else:
            self.assertEqual(self.result_cache.get_user_current_result_id(user_id), new_result_id)

    def test_increment_current_result_id(self):
        self.result_cache.set_user_current_result_id(2, 1)
        self.assertEqual(self.result_cache.increment_current_result_id(1), 3)
        self.assertEqual(self.result_cache.increment_current_result_id(2), 1)

    def test_get_results_keynames(self):
        for i in range(5):
            self.result_cache.set_user_result(i, self.data, 1)

        for keyname, num in zip(self.result_cache.get_results_keynames(1), range(5)):
            self.assertEqual(keyname, f'result:{num}')
