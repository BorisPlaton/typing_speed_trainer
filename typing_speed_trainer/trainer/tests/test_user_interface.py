import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from tests.case_classes.base_case import CacheTestCase
from tests.case_classes.base_live_server import BaseTestLiveServer
from type_results.services import cache_user_typing_result


User = get_user_model()


@pytest.mark.selenium
class TestUserTrainerPage(BaseTestLiveServer, CacheTestCase):

    def test_words_are_loaded(self, web_driver, live_server):
        web_driver.get(live_server.url + reverse('trainer:typing_trainer'))
        WebDriverWait(web_driver, 2).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'select.select-text-language'))
        )
        assert web_driver.find_element(By.CLASS_NAME, "wrd-0")

    def test_results_list_has_label_if_no_results_are_in_cache(self, web_driver, live_server):
        web_driver.get(live_server.url + reverse('trainer:typing_trainer'))
        WebDriverWait(web_driver, 2).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'select.select-text-language'))
        )
        label_with_text = web_driver.find_element(By.CSS_SELECTOR, ".other-user-results-list small")
        assert "Здесь пока ничего нет." in label_with_text.text

    def test_results_list_are_shown_if_cache_has_values(self, web_driver, live_server, user_statistics):
        user = baker.make(User)
        cache_user_typing_result(user.pk, user_statistics)
        web_driver.get(live_server.url + reverse('trainer:typing_trainer'))
        WebDriverWait(web_driver, 2).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'select.select-text-language'))
        )
        assert web_driver.find_element(By.CLASS_NAME, "other-user-results-list .col-lg-12")
