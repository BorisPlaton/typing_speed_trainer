import json

from django.test import TestCase
from django.urls import reverse

from account.models import User
from trainer.utils.datastructures import UserTypingResult
from trainer.utils.cache_results  import TrainerResultCache


class TestRequestStatuses(TestCase):

    def setUp(self) -> None:
        self.credentials = {
            'email': 'test@test.com',
            'password': '12345',
        }

        self.result_data: UserTypingResult = {
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

        self.user = User.objects.create_user(
            **self.credentials,
        )

        self.user_cache_class = TrainerResultCache()
        self.user_cache_class.user_id = self.user.pk

    def tearDown(self):
        self.user_cache_class.delete_current_user_results()

    def test_empty_results_list_from_results_page(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('trainer:results')).json()
        self.assertEqual(response.get('resultsData'), [])

    def test_length_of_results_list_from_results_page(self):
        self.assertTrue(self.client.login(**self.credentials))
        json_data = json.dumps(self.result_data)
        self.client.post(reverse('trainer:results'), json_data, content_type="application/json").json()
        response = self.client.get(reverse('trainer:results')).json()
        self.assertEqual(len(response.get('resultsData')), 1)

    def test_data_of_results_list_from_results_page(self):
        self.assertTrue(self.client.login(**self.credentials))
        json_data = json.dumps(self.result_data)
        self.client.post(reverse('trainer:results'), json_data, content_type="application/json").json()
        response = self.client.get(reverse('trainer:results')).json()
        self.assertEqual(
            response.get('resultsData')[0].get('invalidKeystrokes'), self.result_data.get('invalidKeystrokes')
        )

    def test_data_with_templates_in_results_list_from_results_page(self):
        self.assertTrue(self.client.login(**self.credentials))
        json_data = json.dumps(self.result_data)
        self.client.post(reverse('trainer:results'), json_data, content_type="application/json").json()
        response = self.client.get(reverse('trainer:results') + '?templates=true').json()
        self.assertTrue(response.get('resultsData'))
        self.assertTrue(response.get('resultsListTemplate'))
        self.assertTrue(response.get('resultTemplate'))
