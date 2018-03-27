import pytest
import re
from core.browser_wrapper import visit, get_title, s, get_curl, wait_blockUI, send_javascript_click, refresh, \
    get_source, scroll_to, get_attr_value
from core.conditions import text
from core.etender_data import user_roles
from tests.temp_test_data import TempTestData
import time

@pytest.mark.usefixtures("setup")
class BaseTest(object):
    pass


class BaseOwnerTest(BaseTest):
    pass


class BaseViewerTest(BaseTest):
    pass


class BaseAnonymTest(BaseTest):
    pass


class BaseTestLogic(object):

    def __init__(self, data):
        self._data = data
        self._home_page = self._data.home
        self.temp_data = TempTestData()

    def visit_home(self):
        visit(self._home_page)

    def check_title(self):
        expected_title = self._data.title
        actual_title = get_title()
        assert actual_title == expected_title
        print('\nMethod check_title: Actual result: {0};  Expected: {1}'.format(actual_title, expected_title))

    def fill_login(self, user):
        if user == user_roles.get('owner'):
            user_username = self._data.owner_username
            user_password = self._data.owner_password
        elif user == user_roles.get('viewer1'):
            user_username = self._data.viewer_username
            user_password = self._data.viewer_password
        print('Current user is: {0}'.format(user_username))
        visit(self._home_page + 'login')
        s('#inputUsername').set_value(user_username)
        s('#inputPassword').set_value(user_password)
        s('#btn_submit').click()
        try:
            s('#i_got_it').click()  # skip news
        except:
            pass


    def check_create_from_template_btn(self):
        visit(self._home_page + 'MyTenders')
        wait_blockUI()
        s('a[data-target="#myTenderTemplates"]').click()
        s('#myTenderTemplates h4.modal-title').assure(text, "Оберіть шаблон")


    def add_tender_to_favorite_from_tenderTable(self):
        visit(self._home_page)
        wait_blockUI()
        favorite = get_attr_value('tr:nth-child(1)>td.favorite-td span i', 'class')

        if favorite == 'opacity1':
            print('Tender was already in favorite')
            s('tr:nth-child(1) > td.favorite-td').click()
            scroll_to('down_few')
            s('div[class=\'toast toast-info\'] > div.toast-message').assure(text, "Видалено з обраного")

        s('tr:nth-child(1) > td.favorite-td').click()
        scroll_to('down_few')
        s('div[class=\'toast toast-success\'] > div.toast-message').assure(text, "Додано до обраного")
        self.temp_data.favorite_tender_title = get_attr_value('tr:nth-child(1)>td.title-td.ng-binding > p > a', 'text')
        self.temp_data.favorite_tender_tender_id = re.search('(?=UA)(.*)(?=\xa0\xa0Дата)',
                                                             get_attr_value('tr:nth-child(1)>td.title-td.ng-binding',
                                                                            'innerText', True))[0]
        # go to Обрані закупівлі
        s('a[id="qa_choosedTenders"]').click()
        assert self.temp_data.favorite_tender_title in get_source()
        del self.temp_data

    def add_tender_to_favorite_from_tenderDetailes(self):
        pass


    def go_to_tender(self, tender_link):
        visit(tender_link)
        wait_blockUI()
        s('#naviTitle1').click()
        # s('#collapse-add-docs a').click()
        # opened_url = get_curl()
        # expect = 'http://40.69.95.23/Upload/massAddDocs.pdf'
        # print("Method go_to_tender: Actual result:{0};  Expected: {1}".format(opened_url, expect))
        # assert opened_url == expect


    def add_tender_to_favorite(self):
        wait_blockUI()
        send_javascript_click('addFavorite')
        s('div.toast-message').assure(text, "Додано до обраного")
        tender_title = s('#tenderTitle').text
        tender_id = s('#tenderidua > b').text
        print("Tender title: {0}, TenderId: {1}".format(tender_title, tender_id))
        s('#qa_choosedTenders').click()
        print(str(get_curl()))
        refresh()
        print(str(get_source()))
        assert tender_title, tender_id in get_source()
        # TODO: add assure for '# Видалено з обраного'