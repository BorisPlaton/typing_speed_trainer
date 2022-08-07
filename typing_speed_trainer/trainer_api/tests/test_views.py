from parameterized import parameterized
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from account.models import User
from trainer.utils.cache_results import TrainerResultCache
from trainer.utils.datastructures import UserTypingResult


class TestTemplateFunctionView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'email': 'test@test.com',
            'password': '12345',
        }

        cls.user = User.objects.create_user(
            **cls.credentials,
        )

    def test_result_template(self):
        response = self.client.get(reverse('trainer_api:result_template'))
        self.assertEqual(response.status_code, 403)
        self.client.login(**self.credentials)
        response = self.client.get(reverse('trainer_api:result_template'))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertTrue(response.get('resultTemplate'))
        self.assertFalse(response.get('resultsListTemplate'))

    @parameterized.expand(
        [
            'false',
            'True',
            'tru',
            's2',
            '',
            '2',
        ]
    )
    def test_result_template_list_query_parameter_with_wrong_value(self, list_parameter):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('trainer_api:result_template') + f'?list={list_parameter}')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertTrue(response.get('resultTemplate'))
        self.assertFalse(response.get('resultsListTemplate'))

    def test_result_template_list_query_parameter(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('trainer_api:result_template') + f'?list=true')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertTrue(response.get('resultTemplate'))
        self.assertTrue(response.get('resultsListTemplate'))


class TestResultsListView(APITestCase):

    def setUp(self) -> None:
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
        self.credentials = {
            'email': 'test@test.com',
            'password': '12345',
        }
        self.user = User.objects.create_user(
            **self.credentials,
        )

        self.user_cache_class = TrainerResultCache()
        self.user_cache_class.user_id = self.user.pk

    def tearDown(self) -> None:
        self.user_cache_class.delete_current_user_results()

    def test_request_to_result_page_403_status_code_with_unauthenticated_user(self):
        response = self.client.get(reverse('trainer_api:result-list'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        response = self.client.post(reverse('trainer_api:result-list'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')

    def test_get_request_to_result_page_200_status_code_with_authenticated_user(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('trainer_api:result-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_request_to_result_page_with_authenticated_user_and_data(self):
        self.assertTrue(self.client.login(**self.credentials))
        json_data = json.dumps(self.result_data)
        response = self.client.post(reverse('trainer_api:result-list'), json_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('status'))
        self.assertEqual(response.json().get('status'), 'OK')
        response = self.client.post(reverse('trainer_api:result-list'), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['details'], 'Некорректные данные')

    def test_post_request_to_results_page_400_status_code_with_authenticated_user_but_invalid_wpm_field(self):
        self.assertTrue(self.client.login(**self.credentials))
        self.result_data.update({'wpm': 'invalid wpm'})
        invalid_json_data = json.dumps(self.result_data)
        response = self.client.post(
            reverse('trainer_api:result-list'), invalid_json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_post_request_to_results_page_400_status_code_with_authenticated_user_but_invalid_dateEnd_field(self):
        self.assertTrue(self.client.login(**self.credentials))
        self.result_data.update({'dateEnd': '25-10-2003'})
        invalid_data = self.result_data
        invalid_json_data = json.dumps(invalid_data)
        response = self.client.post(
            reverse('trainer_api:result-list'), invalid_json_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_post_request_to_results_page_415_status_code_with_invalid_content_type_header(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post(reverse('trainer_api:result-list'), self.result_data, content_type="text/plain")
        self.assertEqual(response.status_code, 415)

    def test_empty_results_list_from_results_page(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('trainer_api:result-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('resultsData'), [])

    def test_length_of_results_list_from_results_page(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.post(
            reverse('trainer_api:result-list'),
            json.dumps(self.result_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('trainer_api:result-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('resultsData')), 1)

    def test_data_of_results_list_from_results_page(self):
        self.assertTrue(self.client.login(**self.credentials))
        json_data = json.dumps(self.result_data)
        self.client.post(reverse('trainer_api:result-list'), json_data, content_type="application/json")
        response = self.client.get(reverse('trainer_api:result-list')).json()
        self.assertEqual(
            response.get('resultsData')[0].get('invalidKeystrokes'), self.result_data.get('invalidKeystrokes')
        )
