from core.browser_wrapper import visit
from core.etender_data import homePage, project_titles, viewer_users, owner_users
from tests.base_test import *
from tests.helpers import check_title, fill_login, check_create_from_template_btn

home = homePage.get('QA', {}).get('RialtoQA')
title = project_titles.get("TitleRialto")
owner_username = owner_users.get("username")
owner_password = owner_users.get("password")
viewer_username = viewer_users.get("username")
viewer_password = viewer_users.get("password")


class TestLoginRialtoAuction(BaseTest):

    def test_visit_home(self):
        visit(home)

    def test_check_title(self):
        check_title(title)

    def test_fill_login(self):
        fill_login(home, customer_username, customer_password)

    def test_can_create_from_template(self):
        check_create_from_template_btn()