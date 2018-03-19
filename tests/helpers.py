import time

from core import config
from core.browser_wrapper import visit, get_curl, s, get_title, wait_blockUI, send_javascript_click, get_source, refresh
from core.conditions import text, visible, clickable


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


# def check_create_from_template_btn(home_page):
#     assert get_curl() == home_page + 'MyTenders'
#     s('a[data-target="#myTenderTemplates"]').click()
#     s('#myTenderTemplates h4.modal-title').assure(text, "Оберіть шаблон")


def go_to_tender(tender_link):
    visit(tender_link)
    wait_blockUI()
    s('#naviTitle1').click()
    # s('#collapse-add-docs a').click()
    # opened_url = get_curl()
    # expect = 'http://40.69.95.23/Upload/massAddDocs.pdf'
    # print("Method go_to_tender: Actual result:{0};  Expected: {1}".format(opened_url, expect))
    # assert opened_url == expect


def check_bidButton_for_anonym(home):
    visit(home)
    s('a .bidButton-fixed cp ng-scope').assure(clickable).click()
    assert get_curl() == home + 'register'
