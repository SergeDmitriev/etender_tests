import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from UiTests.core import config


@pytest.fixture(scope='class')
def setup(request):
    config.browser = webdriver.Chrome()
    config.browser.maximize_window()
    config.browser.implicitly_wait(5)
    config.wait = WebDriverWait(config.browser, config.timeout)

    def teardown():
        config.browser.quit()

    request.addfinalizer(teardown)
