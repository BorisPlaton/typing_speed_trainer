import json

from django.test import TestCase
from django.urls import reverse

from account.models import User
from trainer.utils.datastructures import UserTypingResult
from trainer.utils.cache_results import TrainerResultCache


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

    def tearDown(self) -> None:
        self.user_cache_class.delete_current_user_results()

    def test_typing_trainer_page_200_status_code_with_unauthenticated_user(self):
        response = self.client.get(reverse('trainer:typing_trainer'))
        self.assertEqual(response.status_code, 200)

    def test_typing_trainer_page_200_status_code_with_authenticated_user(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('trainer:typing_trainer'))
        self.assertEqual(response.status_code, 200)

    def test_get_request_to_results_page_302_status_code_with_unauthenticated_user(self):
        response = self.client.get(reverse('trainer:results'))
        self.assertEqual(response.status_code, 302)

    def test_get_request_to_results_page_200_status_code_with_authenticated_user(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('trainer:results'))
        self.assertEqual(response.status_code, 200)

    def test_get_request_to_results_page_200_status_code_with_authenticated_user_and_query_parameters(self):
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get(reverse('trainer:results') + '?templates=true')
        self.assertEqual(response.status_code, 200)

    def test_post_request_to_results_page_302_status_code_with_unauthenticated_user(self):
        response = self.client.post(reverse('trainer:results'))
        self.assertEqual(response.status_code, 302)

    def test_post_request_to_results_page_200_status_code_with_authenticated_user_and_data(self):
        self.assertTrue(self.client.login(**self.credentials))
        json_data = json.dumps(self.result_data)
        response = self.client.post(reverse('trainer:results'), json_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_post_request_to_results_page_400_status_code_with_authenticated_user_but_invalid_wpm_field(self):
        self.assertTrue(self.client.login(**self.credentials))
        self.result_data.update({'wpm': 'invalid wpm'})
        invalid_data = self.result_data
        invalid_json_data = json.dumps(invalid_data)
        response = self.client.post(reverse('trainer:results'), invalid_json_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_post_request_to_results_page_400_status_code_with_authenticated_user_but_invalid_dateEnd_field(self):
        self.assertTrue(self.client.login(**self.credentials))
        self.result_data.update({'dateEnd': '25-10-2003'})
        invalid_data = self.result_data
        invalid_json_data = json.dumps(invalid_data)
        response = self.client.post(reverse('trainer:results'), invalid_json_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_post_request_to_results_page_412_status_code_with_invalid_content_type_header(self):
        self.assertTrue(self.client.login(**self.credentials))
        invalid_json_data = json.dumps(self.result_data)
        response = self.client.post(reverse('trainer:results'), invalid_json_data, content_type="text/plain")
        self.assertEqual(response.status_code, 412)
