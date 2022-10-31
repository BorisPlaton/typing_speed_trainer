import os
import shutil
from enum import Enum, auto
from os import path
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.remote.webdriver import WebDriver


class WebDriverTypes(Enum):
    FIREFOX = auto()


@pytest.mark.django_db
class BaseTestLiveServer:

    @pytest.fixture(scope='class', autouse=True)
    def tmpdir_make(self):
        tmp_dir_path = Path(__file__).parent.parent / 'tmpdir'
        try:
            os.mkdir(tmp_dir_path)
            os.environ['TMPDIR'] = str(tmp_dir_path)
            yield
        finally:
            shutil.rmtree(tmp_dir_path)

    @pytest.fixture
    def web_driver(self, _driver) -> WebDriver:
        with _driver as configured_driver:
            yield configured_driver

    @pytest.fixture(params=[WebDriverTypes.FIREFOX])
    def _driver(self, request):
        if request.param == WebDriverTypes.FIREFOX:
            service = Service(GeckoDriverManager().install(), log_path=path.devnull)
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            return webdriver.Firefox(service=service, options=options)
        raise ValueError(f"Unknown webdriver type {request.param} was given.")
