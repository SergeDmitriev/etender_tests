import time

from core import config
from core.browser_wrapper import visit, get_curl, s, get_title, wait_blockUI, send_javascript_click, get_source
from core.conditions import text, visible


def check_title(expected_title):
    actual_title = get_title()
    assert actual_title == expected_title
    print('Method check_title: Actual result: {0};  Expected: {1}'.format(actual_title, expected_title))


def fill_login(homepage, username, password):
    visit(homepage + 'login')
    s('#inputUsername').set_value(username)
    s('#inputPassword').set_value(password)
    s('#btn_submit').click()
    try:
        s('#i_got_it').click()  # skip news
    except:
        pass


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
    s('a[data-target="#myTenderTemplates"]').click()
    s('#myTenderTemplates h4.modal-title').assure(text, "Оберіть шаблон")


def go_to_tender(tender_link):
    visit(tender_link)
    wait_blockUI()
    s('#naviTitle1').click()
    # s('#collapse-add-docs a').click()
    # opened_url = get_curl()
    # expect = 'http://40.69.95.23/Upload/massAddDocs.pdf'
    # print("Method go_to_tender: Actual result:{0};  Expected: {1}".format(opened_url, expect))
    # assert opened_url == expect


def add_tender_to_favorite():
    wait_blockUI()
    send_javascript_click('addFavorite')
    s('div.toast-message').assure(text, "Додано до обраного")
    tender_title = s('#tenderTitle').text
    tender_id = s('#tenderidua > b').text
    print("Tender title: {0}, TenderId: {1}".format(tender_title, tender_id))
    time.sleep(10)
    s('#qa_choosedTenders').click()
    time.sleep(5)
    print(str(get_curl()))
    print(str(get_source()))
    assert tender_title, tender_id in get_source()

# Видалено з обраного