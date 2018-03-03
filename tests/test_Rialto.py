from core.browser_wrapper import visit
from core.etender_data import homePage, users
from tests.base_test import *
from tests.helpers import check_title, fill_login

home = homePage.get("Rialto")
customer_username = users.get("username")
customer_password = users.get("password")


class TestLoginProzorro(BaseTest):

    def test_visit_home(self):
        visit(home)
        check_title()

    def test_fill_login(self):
        fill_login(home, customer_username, customer_password)




