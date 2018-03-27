from core.etender_data import ProzorroData
from tests.base_test_logic import *


class TestProzorroOwner(BaseOwnerTest):

    d = BaseTestLogic(ProzorroData)
    user = user_roles.get('owner')

    def test_visit_home(self):
        self.d.visit_home()
        self.d.check_title()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    def test_can_create_from_template(self):
        self.d.check_create_from_template_btn()


class TestProzorroViewer(BaseViewerTest):

    d = BaseTestLogic(ProzorroData)
    user = user_roles.get('viewer1')

    def test_visit_home(self):
        self.d.visit_home()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    def test_add_tender_to_favorite_from_tenderTable(self):
        self.d.add_tender_to_favorite_from_tenderTable()

    def test_add_tender_to_favorite_from_tenderDetailes(self):
        self.d.add_tender_to_favorite_from_tenderDetailes()

    # def test_go_to_tender(self):
    #     self.d.go_to_tender("http://40.69.95.23/#/tenderDetailes/48881cb3582e4049b5e2db33f931fd03")




class TestProzorroAnonym(BaseAnonymTest):

    d = BaseTestLogic(ProzorroData)
    user = user_roles.get('anonym')

    def test_visit_home(self):
        self.d.visit_home()

    def test_check_bid_btn_for_anonym(self):
        self.d.check_bidButton_for_anonym()