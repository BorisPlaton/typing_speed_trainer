
class TestCurrentUserCache(TestCase):

    def setUp(self) -> None:
        ResultCache.cache_base_name = 'test'
        self.current_user_cache = CurrentUserCache()
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
        ResultCache.clean_cache()

    def test_current_user_result_id(self):
        for i in range(5):
            self.current_user_cache._set_user_current_result_id(i, i)

        self.assertEqual(
            self.current_user_cache.user_current_result_id, self.current_user_cache.user_id
        )

    def test_difference_between_different_users_using_current_user_result_id(self):
        self.current_user_cache.increment_user_result_id()
        first_user_result_id = self.current_user_cache.user_current_result_id

        self.current_user_cache.user_id = 2
        self.current_user_cache._set_user_current_result_id(4, 2)
        second_user_result_id = self.current_user_cache.user_current_result_id

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
            self.current_user_cache.add_user_result(data)
        self.assertTrue(self.current_user_cache.get_all_user_results())

        self.current_user_cache.user_id = 2
        self.assertFalse(self.current_user_cache.get_all_user_results())

        self.current_user_cache.user_id = 1

        for data in user_data:
            self.assertTrue(data in self.current_user_cache.get_all_user_results())
