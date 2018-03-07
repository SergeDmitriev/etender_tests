from core.browser_wrapper import visit
from core.etender_data import homePage, users, project_titles
from tests.base_test import *
from tests.helpers import check_title, fill_login

home = homePage.get('QA', {}).get('RialtoAuctionQA')
customer_username = users.get("username")
customer_password = users.get("password")
title = project_titles.get("TitleRialtoAuction")


class TestLoginRialtoAuction(BaseTest):

    def test_visit_home(self):
        visit(home)

    def test_check_title(self):
        check_title(title)

    def test_fill_login(self):
        fill_login(home, customer_username, customer_password)
