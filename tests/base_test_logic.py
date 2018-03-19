import pytest
from core.browser_wrapper import visit, get_title, s, get_curl, wait_blockUI, send_javascript_click, refresh, get_source
from core.conditions import text
from core.etender_data import user_roles


@pytest.mark.usefixtures("setup")
class BaseTest(object):
    pass


class BaseOwnerTest(BaseTest):
    pass


class BaseViewerTest(BaseTest):
    pass





class BaseTestLogic(object):

    def __init__(self, data):
        self._data = data
        self._home_page = self._data.home

    def visit_home(self):
        visit(self._home_page)

    def check_title(self):
        expected_title = self._data.title
        actual_title = get_title()
        assert actual_title == expected_title
        print('Method check_title: Actual result: {0};  Expected: {1}'.format(actual_title, expected_title))

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
        assert get_curl() == self._home_page + 'MyTenders'
        s('a[data-target="#myTenderTemplates"]').click()
        s('#myTenderTemplates h4.modal-title').assure(text, "Оберіть шаблон")

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