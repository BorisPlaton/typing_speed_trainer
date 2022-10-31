import pytest
from django.urls import reverse
from model_bakery import baker
from selenium.webdriver.common.by import By

from account.models import User
from account.views import UsersList
from tests.case_classes.base_live_server import BaseTestLiveServer


@pytest.mark.selenium
class TestAccountList(BaseTestLiveServer):

    def test_if_none_users_present_list_page_has_special_label(self, web_driver, live_server):
        web_driver.get(live_server.url + reverse('account:users'))
        element = web_driver.find_element(By.CSS_SELECTOR, '.row p')
        assert element.text == "Пока нет никаких пользователей. Станьте первым!"

    def test_first_second_third_users_has_special_borders(self, web_driver, live_server):
        baker.make(User, _quantity=4)
        web_driver.get(live_server.url + reverse('account:users'))

        fist_user_div = web_driver.find_element(By.CSS_SELECTOR, 'div.col-lg-3.col-4:nth-child(1)')
        second_user_div = web_driver.find_element(By.CSS_SELECTOR, 'div.col-lg-3.col-4:nth-child(2)')
        third_user_div = web_driver.find_element(By.CSS_SELECTOR, 'div.col-lg-3.col-4:nth-child(3)')
        fourth_user_div = web_driver.find_element(By.CSS_SELECTOR, 'div.col-lg-3.col-4:nth-child(4)')

        assert 'border-yellow-300' in fist_user_div.find_element(
            By.CSS_SELECTOR, 'div.rounded-bottom'
        ).get_attribute('class')

        assert 'border-main-600' in second_user_div.find_element(
            By.CSS_SELECTOR, 'div.rounded-bottom'
        ).get_attribute('class')

        assert 'border-main-400' in third_user_div.find_element(
            By.CSS_SELECTOR, 'div.rounded-bottom'
        ).get_attribute('class')

        assert 'border-blue-800' in fourth_user_div.find_element(
            By.CSS_SELECTOR, 'div.rounded-bottom'
        ).get_attribute('class')

    def test_on_another_page_all_users_has_regular_borders(self, web_driver, live_server):
        baker.make(User, _quantity=UsersList.paginate_by + 4)
        web_driver.get(live_server.url + reverse('account:users') + '?page=2')
        for child_num in range(1, 4):
            assert 'border-blue-800' in web_driver.find_element(
                By.CSS_SELECTOR, f'div.col-lg-3.col-4:nth-child({child_num})'
            ).find_element(By.CSS_SELECTOR, "div.rounded-bottom").get_attribute('class')
