from core import config
from core.elements import SmartElement, SmartElementsCollection
from core.conditions import present


def visit(url):
    config.browser.get(url)


def refresh():
    config.browser.refresh()


def get_curl():
    return config.browser.current_url


def close():
    config.browser.close()


def s(locator):
    return SmartElement(locator)


def ss(locator):
    return SmartElementsCollection(locator)


def until_not(locator, condition):
    config.wait.until_not(condition(locator))
    return locator


def wait_ui():
    # TODO: refactor
    until_not(s('.blockUI'), present)


def until(locator, condition):
    config.wait.until(condition(locator))
    return locator


def scroll_to_bottom():
    config.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


