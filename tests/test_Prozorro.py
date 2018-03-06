from core.browser_wrapper import visit
from core.etender_data import homePage, users, project_titles
from core.managers import BaseOwnerManager
from tests.base_test import *
from tests.helpers import check_title, fill_login, go_to_tender

home = homePage.get("Prozorro")
customer_username = users.get("username")
customer_password = users.get("password")
title = project_titles.get("TitleProzorro")

class TestLoginProzorro(BaseTest):

    owner = BaseOwnerManager("owner", "case6", "Qq123456")

    def test_visit_home(self):
        visit(home)

    def test_check_title(self):
        check_title(title)

    def test_fill_login(self, owner=BaseOwnerManager("owner", "case6", "Qq123456")):
        # fill_login(home, customer_username, customer_password)
        fill_login(home, owner.username, owner.password)

    def test_go_to_tender(self):
        go_to_tender("http://40.69.95.23/#/tenderDetailes/8b99050fbe644b6cb4decc81d069a4d0")
