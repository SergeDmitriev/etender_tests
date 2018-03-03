import time
from core import config
from core.browser_wrapper import visit


def check_title():
    title = config.browser.title
    # assert title in 'Державні закупівлі'


def fill_login(homepage, username, password):
    visit(homepage+'login')
    time.sleep(3)
    config.browser.find_element_by_id('inputUsername').send_keys(username)
    config.browser.find_element_by_id('inputPassword').send_keys(password)
    config.browser.find_element_by_id('btn_submit').click()