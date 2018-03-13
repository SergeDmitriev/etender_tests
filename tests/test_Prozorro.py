from core.browser_wrapper import visit
from core.etender_data import homePage, project_titles, viewer_users, owner_users
from tests.base_test import *
from tests.helpers import check_title, fill_login, create_owner, check_create_from_template_btn, create_viewer, \
    go_to_tender, add_tender_to_favorite

home = homePage.get('QA', {}).get('ProzorroQA')
title = project_titles.get("TitleProzorro")
owner_username = owner_users.get("username")
owner_password = owner_users.get("password")
viewer_username = viewer_users.get("username")
viewer_password = viewer_users.get("password")


class TestLoginProzorro(BaseOwnerTest):

    current_owner = create_owner(owner_username, owner_password)

    def test_visit_home(self):
        visit(home)
        check_title(title)

    def test_fill_login(self):
        fill_login(home, self.current_owner.username, self.current_owner.password)

    def test_can_create_from_template(self):
        check_create_from_template_btn()





class TestLoginProzorroViewer(BaseViewerTest):

    current_viewer = create_viewer(viewer_username, viewer_password)

    def test_visit_home(self):
        visit(home)

    def test_fill_login(self):
        fill_login(home, self.current_viewer.username, self.current_viewer.password)

    def test_go_to_tender(self):
        go_to_tender("http://40.69.95.23/#/tenderDetailes/48881cb3582e4049b5e2db33f931fd03")

    def test_add_tender_to_favorite(self):
        add_tender_to_favorite()