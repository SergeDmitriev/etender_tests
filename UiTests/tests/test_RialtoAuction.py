from UiTests.core.etender_data import RialtoAuctionData
from UiTests.tests.base_test_logic import *


class TestRialtoAuctionOwner(BaseTest):

    d = BaseTestLogic(RialtoAuctionData)
    user = user_roles.get('owner')

    def test_visit_home(self):
        self.d.visit_home()
        self.d.check_title()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    def test_can_create_from_template(self):
        self.d.check_create_from_template_btn()


class TestRialtoAuctionViewer(BaseViewerTest):

    d = BaseTestLogic(RialtoAuctionData)
    user = user_roles.get('viewer1')

    def test_visit_home(self):
        self.d.visit_home()

    def test_fill_login(self):
        self.d.fill_login(self.user)

    def test_add_tender_to_favorite_from_tenderTable(self):
        self.d.add_tender_to_favorite_from_tenderTable()

    def test_add_tender_to_favorite_from_tenderDetailes(self):
        self.d.add_tender_to_favorite_from_tenderDetailes()


class TestRialtoAuctionAnonym(BaseAnonymTest):

    d = BaseTestLogic(RialtoAuctionData)
    user = user_roles.get('anonym')

    def test_visit_home(self):
        self.d.visit_home()

    def test_check_bid_btn_for_anonym(self):
        self.d.check_bidButton_for_anonym()