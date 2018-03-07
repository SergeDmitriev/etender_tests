from core.browser_wrapper import visit
from core.etender_data import homePage, project_titles, viewer_users
from tests.base_test import *
from tests.helpers import check_title, fill_login, go_to_tender, create_owner

home = homePage.get('QA', {}).get('ProzorroQA')

customer_username = viewer_users.get("username")
customer_password = viewer_users.get("password")
title = project_titles.get("TitleProzorro")

class TestLoginProzorro(BaseTest):

    current_owner = create_owner(customer_username, customer_password)

    def test_create_test_user(self):
        pass

    def test_visit_home(self):
        visit(home)

    def test_check_title(self):
        check_title(title)

    def test_fill_login(self):
        # fill_login(home, customer_username, customer_password)
        fill_login(home, self.current_owner.username, self.current_owner.password)

    def test_go_to_tender(self):
        go_to_tender("http://40.69.95.23/#/tenderDetailes/765d89c8494844f2a9420d70845d7fa3")
