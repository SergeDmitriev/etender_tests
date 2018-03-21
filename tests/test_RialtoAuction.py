from core.etender_data import RialtoAuctionData, user_roles
from tests.base_test_logic import *
from tests.helpers import check_bidButton_for_anonym


class TestLoginRialtoAuctionOwner(BaseTest):

    d = BaseTestLogic(RialtoAuctionData)
    user = user_roles.get('owner')

    def test_visit_home(self):
        self.d.visit_home()
        self.d.check_title()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    def test_can_create_from_template(self):
        self.d.check_create_from_template_btn()


class TestLoginRialtoAuctionViewer(BaseViewerTest):

    d = BaseTestLogic(RialtoAuctionData)
    user = user_roles.get('viewer1')

    def test_visit_home(self):
        self.d.visit_home()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    def test_go_to_tender(self):
        self.d.go_to_tender('')

    def test_add_tender_to_favorite(self):
        self.d.add_tender_to_favorite()