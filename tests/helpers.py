import time
from core import config
from core.browser_wrapper import visit, get_curl, s


def check_title(get_title):
    title = config.browser.title
    assert title == get_title
    print('Method check_title: Actual result: {0};  Expected: {1}'.format(get_title, title))


def fill_login(homepage, username, password):
    visit(homepage + 'login')
    s('#inputUsername').set_value(username)
    s('#inputPassword').set_value(password)
    s("btn_submit").click()
    try:
        s('#i_got_it').click()  # skip news
    except:
        pass
    time.sleep(5)


def go_to_tender(tender_link):
    visit(tender_link)
    time.sleep(5)
    # config.browser.find_element_by_id("tenderTitle") == "[ТЕСТУВАННЯ] 2 lot, 2 bids"
    s('#naviTitle1').click()
    time.sleep(4)
    s('#collapse-add-docs a').click()
    time.sleep(2)

    opened_url = get_curl()
    expect = 'http://40.69.95.23/Upload/massAddDocs.pdf'
    print("Method go_to_tender: Actual result:{0};  Expected: {1}".format(opened_url, expect))
    assert opened_url == expect



def print_to_console_username(login):
        ("Current user is: ", login)

def create_owner(username, password):
    from core.managers import OwnerManager
    owner = OwnerManager("owner", username, password)
    print_to_console_username(owner.username)
    return owner

def create_viewer(username, password):
    from core.managers import ViewerManager
    viewer = ViewerManager("owner", username, password)
    print_to_console_username(viewer.username)
    return viewer

def check_create_from_template_btn():
    assert get_curl() == 'http://40.69.95.23/#/MyTenders'
    time.sleep(2)
    s('a[data-target="#myTenderTemplates"]').click()
    a = config.browser.find_element_by_css_selector('#myTenderTemplates h4.modal-title').text
    print(a)
    s('.list-group-item')
    assert "Оберіть шаблон" in a


