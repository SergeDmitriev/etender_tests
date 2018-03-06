import time
from core import config
from core.browser_wrapper import visit, get_curl


def check_title(get_title):
    title = config.browser.title
    assert title == get_title
    print('Method check_title: Actual result: {0};  Expected: {1}'.format(get_title, title))


def fill_login(homepage, username, password):
    visit(homepage+'login')
    # time.sleep(3)
    config.browser.find_element_by_id('inputUsername').send_keys(username)
    config.browser.find_element_by_id('inputPassword').send_keys(password)
    config.browser.find_element_by_id('btn_submit').click()
    time.sleep(5)


def go_to_tender(tender_link):
    visit(tender_link)
    time.sleep(5)
    # config.browser.find_element_by_id("tenderTitle") == "[ТЕСТУВАННЯ] 2 lot, 2 bids"
    config.browser.find_element_by_id("naviTitle1").click()
    time.sleep(4)
    config.browser.find_element_by_css_selector("#collapse-add-docs a").click()
    time.sleep(2)
    
    opened_url = get_curl()
    expect = 'http://40.69.95.23/Upload/massAddDocs.pdf'
    print("Method go_to_tender: Actual result:{0};  Expected: {1}".format(opened_url, expect))
    assert opened_url == expect



