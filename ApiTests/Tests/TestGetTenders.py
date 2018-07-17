from ApiTests.Application.Tender import Tender
from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.app_config import universal_password, division_admin_login


class TestGetTenders(BaseApiTestLogic):
    tender = Tender(division_admin_login, universal_password)

    def test_get_tenders(self, get_tenders_tab_parametrized):
        # TODO: add assert with db in count (elastic and db result differs)

        result = self.tender.get_tenders(tab=get_tenders_tab_parametrized['tab'],
                                         mode=get_tenders_tab_parametrized['mode'],
                                         is_real_tenders_for_test_mode=get_tenders_tab_parametrized[
                                             'show_real_checkbox'])
        print('Tenders count :', self.tender.count_all_records(result))

    # def test_log_out(self):
    #     print(self.tender.headers)
    #     print(self.tender.log_out_user(self.tender.headers))
