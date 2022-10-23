import pytest
from django.urls import reverse
from rest_framework.utils import json

from tests.utils import BaseTestCase


class TestTemplateFunctionView(BaseTestCase):

    def test_result_template(self, credentials, api_client):
        response = api_client.get(reverse('trainer_api:result_template'))
        assert response.status_code == 403
        api_client.login(**credentials)
        response = api_client.get(reverse('trainer_api:result_template'))
        assert response.status_code == 200
        response = json.loads(response.content)
        assert response.get('resultTemplate')
        assert not response.get('resultsListTemplate')

    @pytest.mark.parametrize(
        'list_parameter',
        ['false', 'True', 'tru', 's2', '', '2', ]
    )
    def test_result_template_list_query_parameter_with_wrong_value(self, list_parameter, api_client, login):
        response = api_client.get(reverse('trainer_api:result_template') + f'?list={list_parameter}')
        assert response.status_code == 200
        response = json.loads(response.content)
        assert response.get('resultTemplate')
        assert not response.get('resultsListTemplate')

    def test_result_template_list_query_parameter(self, api_client, login):
        response = api_client.get(reverse('trainer_api:result_template') + '?list=true')
        assert response.status_code == 200
        response = json.loads(response.content)
        assert response.get('resultTemplate')
        assert response.get('resultsListTemplate')


class TestResultsListView(BaseTestCase):

    def test_request_to_result_page_403_status_code_with_unauthenticated_user(self, api_client):
        response = api_client.get(reverse('trainer_api:result-list'))
        assert response.status_code == 403
        assert response.json()['detail'] == 'Authentication credentials were not provided.'
        response = api_client.post(reverse('trainer_api:result-list'))
        assert response.status_code == 403
        assert response.json()['detail'] == 'Authentication credentials were not provided.'

    def test_get_request_to_result_page_200_status_code_with_authenticated_user(self, api_client, login):
        response = api_client.get(reverse('trainer_api:result-list'))
        assert response.status_code == 200

    def test_post_request_to_result_page_with_authenticated_user_and_data(
            self, user_statistics_dict, api_client, login
    ):
        json_data = json.dumps(user_statistics_dict)
        response = api_client.post(reverse('trainer_api:result-list'), json_data, content_type="application/json")
        assert response.status_code == 200
        assert response.json().get('status')
        assert response.json().get('status') == 'OK'
        response = api_client.post(reverse('trainer_api:result-list'), content_type="application/json")
        assert response.status_code == 400
        assert response.json()['details']

    def test_post_request_to_results_page_400_status_code_with_authenticated_user_but_invalid_wpm_field(
            self, user_statistics_dict, api_client, login
    ):
        user_statistics_dict.update({'wpm': 'invalid wpm'})
        invalid_json_data = json.dumps(user_statistics_dict)
        response = api_client.post(
            reverse('trainer_api:result-list'), invalid_json_data, content_type="application/json"
        )
        assert response.status_code, 400

    def test_empty_results_list_from_results_page_if_no_data_exists(self, api_client, login):
        response = api_client.get(reverse('trainer_api:result-list'))
        assert response.status_code == 200
        assert response.json().get('resultsData') == []

    def test_length_of_results_list_from_results_page(self, user_statistics_dict, api_client, login):
        response = api_client.post(
            reverse('trainer_api:result-list'),
            json.dumps(user_statistics_dict), content_type="application/json"
        )
        assert response.status_code == 200
        response = api_client.get(reverse('trainer_api:result-list'))
        assert response.status_code == 200
        assert len(response.json().get('resultsData')) == 1

    def test_data_of_results_list_from_results_page(self, user_statistics_dict, api_client, login):
        json_data = json.dumps(user_statistics_dict)
        api_client.post(reverse('trainer_api:result-list'), json_data, content_type="application/json")
        response = api_client.get(reverse('trainer_api:result-list')).json()
        assert response.get('resultsData')[0].get('invalidKeystrokes') == user_statistics_dict.get('invalidKeystrokes')
