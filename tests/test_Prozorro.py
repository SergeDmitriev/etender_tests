from core.etender_data import ProzorroData, user_roles
from tests.base_test_logic import *
from tests.helpers import check_bidButton_for_anonym


class TestLoginProzorroOwner(BaseOwnerTest):

    d = BaseTestLogic(ProzorroData)
    user = user_roles.get('owner')

    def test_visit_home(self):
        self.d.visit_home()
        self.d.check_title()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    def test_click_first_tender_for_add_to_favorite(self):
        self.d.click_first_tender_for_add_to_favorite()

    # def test_can_create_from_template(self):
    #     self.d.check_create_from_template_btn()


class TestLoginProzorroViewer(BaseViewerTest):

    d = BaseTestLogic(ProzorroData)
    user = user_roles.get('viewer1')

    def test_visit_home(self):
        self.d.visit_home()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    # def test_go_to_tender(self):
    #     self.d.go_to_tender("http://40.69.95.23/#/tenderDetailes/48881cb3582e4049b5e2db33f931fd03")

    def test_add_tender_to_favorite(self):
        self.d.add_tender_to_favorite()


    # def test_check_bidButton_for_anonym(self):
    #     check_bidButton_for_anonym(home)
