from core.browser_wrapper import visit
from core.etender_data import homePage, project_titles, viewer_users, owner_users
from tests.base_test import *
from tests.helpers import check_title, fill_login, go_to_tender, create_owner, check_create_from_template_btn

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

    def test_check_title(self):
        check_title(title)

    def test_fill_login(self):
        fill_login(home, self.current_owner.username, self.current_owner.password)

    def test_can_create_from_template(self):
        check_create_from_template_btn()




    # def test_go_to_tender(self):
    #     go_to_tender("http://40.69.95.23/#/tenderDetailes/765d89c8494844f2a9420d70845d7fa3")





# class TestLoginProzorroViewer(BaseViewerTest):
#
#     current_viewer = create_viewer(viewer_username, viewer_password)
#
#     def test_visit_home(self):
#         visit(home)
