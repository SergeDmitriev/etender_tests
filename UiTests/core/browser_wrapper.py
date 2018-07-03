from UiTests.core import config
from UiTests.core.elements import SmartElement, SmartElementsCollection
from UiTests.core.conditions import present
from selenium.common.exceptions import NoSuchElementException

#Base commands:
def visit(url):
    config.browser.get(url)
    wait_blockUI()


def refresh():
    config.browser.refresh()
    wait_blockUI()


def get_curl():
    return config.browser.current_url


def get_title():
    return config.browser.title


def get_source():
    return config.browser.page_source


def close():
    config.browser.close()


def get_attr_value(element, attribute_name, print_attr=False):
    try:
        attribute_value = s(element).assure(present).get_attribute(attribute_name)
        if print_attr == True:
            print('Element.Attribute.Value is : ', attribute_value + '\n')
        return attribute_value
    except:
        print_exception()
        return None


def print_exception():
    import traceback
    traceback.print_exc()


def whoami():
    import sys
    return sys._getframe(2).f_code.co_name
    #2 - callersname


#SmartElements:
def s(locator):
    return SmartElement(locator)


def ss(locator):
    return SmartElementsCollection(locator)


def until_not(locator, condition):
    config.wait.until_not(condition(locator))
    return locator


def wait_blockUI():
    # TODO: refactor
    until_not(s('.blockUI'), present)


def until(locator, condition):
    config.wait.until(condition(locator))
    return locator


def check_exist(css_selector):
    try:
        s(css_selector)
    except NoSuchElementException:
        return False
    return None


#JavaScript commands:
def send_javascript_click(element):
    javascript_command = str("javascript:document.getElementById('{0}').click();").format(element)
    config.browser.execute_script(javascript_command)


def scroll_to(pos='down'):
    """Possible values:
    - top
    - top_few
    - down
    - down_few"""
    if pos=='top':
        config.browser.execute_script("window.scrollTo(0, 0);")
    elif pos == 'down_few':
        config.browser.execute_script("window.scrollBy(0,10)")
    elif pos == 'top_few':
        config.browser.execute_script("window.scrollBy(0,-10)")
    else:
        config.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# def handle_alert(key):
#     alert_text = Alert(config.browser)
#     if key == 'accept':
#         print('Alert text captured: ', alert_text)
#         Alert(config.browser).accept()
#     elif key == 'dismiss':
#         print('Alert text captured: ', alert_text)
#         Alert(config.browser).dismiss()
#     else:
#         print('Alert text captured: ', alert_text)
#         return alert_text


def get_javascript_cur_page():
    return config.browser.execute_script("return window.location.href;")