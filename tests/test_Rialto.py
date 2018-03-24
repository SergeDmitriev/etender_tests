from core.etender_data import RialtoData, user_roles
from tests.base_test_logic import *
from tests.helpers import check_bidButton_for_anonym


class TestLoginRialtoOwner(BaseTest):

    d = BaseTestLogic(RialtoData)
    user = user_roles.get('owner')

    def test_visit_home(self):
        self.d.visit_home()
        self.d.check_title()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    def test_click_first_tender_for_add_to_favorite(self):
        self.d.add_tender_to_favorite_from_tenderTable()




    # def test_can_create_from_template(self):
    #     self.d.check_create_from_template_btn()


class TestLoginRialtoViewer(BaseViewerTest):

    d = BaseTestLogic(RialtoData)
    user = user_roles.get('viewer1')

    def test_visit_home(self):
        self.d.visit_home()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    def test_add_tender_to_favorite(self):
        self.d.add_tender_to_favorite()


    # def test_check_bidButton_for_anonym(self):
    #     check_bidButton_for_anonym(home)