import pytest
import re
from UiTests.core.browser_wrapper import visit, get_title, s, wait_blockUI, \
    get_source, scroll_to, get_attr_value, get_javascript_cur_page, refresh
from UiTests.core.conditions import text
from UiTests.core.etender_data import user_roles
from UiTests.tests.temp_test_data import TempTestData


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
        tender = get_attr_value('tr:nth-child(1)>td.title-td.ng-binding > p > a', 'text')
        print(tender)
        s('a[id="qa_choosedTenders"]').click()
        assert self.temp_data.favorite_tender_title in get_source()

    def add_tender_to_favorite_from_tenderDetailes(self):
        visit(self._home_page)
        refresh()
        s('tr:nth-child(1) > td.title-td.ng-binding > p > a').click()
        print('Method add_tender_to_favorite_from_tenderDetailes: TenderURL: ', get_javascript_cur_page())
        favorite = get_attr_value('#addFavorite', 'class')

        # if favorite == 'opacity1':
        #     print('Tender was already in favorite')
        #     s('span[class=\'favorite favorite-max\'] > i[id="addFavorite"]').assure(clickable).click()
        #     scroll_to('down_few')
        #     s('div[class=\'toast toast-info\'] > div.toast-message').assure(text, "Видалено з обраного")
        #
        # s('span[class=\'favorite favorite-max\'] > i[id="addFavorite"]').assure(clickable).click()
        # scroll_to('down_few')
        # s('div[class=\'toast toast-success\'] > div.toast-message').assure(text, "Додано до обраного")
        # self.temp_data.favorite_tender_title = get_attr_value('h1[id=\'tenderTitle\']', 'text')
        # self.temp_data.favorite_tender_tender_id = re.search('(?=UA)(.*)(?=\xa0\xa0Дата)',
        #                                                      get_attr_value('span > b',
        #                                                                     'innerText', True))[0]


#Anonym functionality
    def check_bidButton_for_anonym(self):
        wait_blockUI()
        s('tr:nth-child(1) > td.title-td.ng-binding > p > a').click()
        wait_blockUI()
        print('Method bidButton_for_anonym. TenderURL: ', get_javascript_cur_page())
        s('a[class=\'bidButton-fixed cp ng-scope\']').click()
        self.temp_data.anonym_tender_bidBtn = get_javascript_cur_page()
        assert self.temp_data.anonym_tender_bidBtn == self._home_page + 'register'


    def check_mvs_link(self):
        pass

    # def go_to_tender(self, tender_link):
    #     visit(tender_link)
    #     wait_blockUI()
    #     s('#naviTitle1').click()
    #     # s('#collapse-add-docs a').click()
        # opened_url = get_curl()
        # expect = 'http://40.69.95.23/Upload/massAddDocs.pdf'
        # print("Method go_to_tender: Actual result:{0};  Expected: {1}".format(opened_url, expect))
        # assert opened_url == expect