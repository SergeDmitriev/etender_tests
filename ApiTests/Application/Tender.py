from requests import post

from ApiTests.Application.Models.GetTendersModel import GetTendersModel, GetTendersWithResponsiblesModel
from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Helpers import body_to_dict
from ApiTests.app_config import production_mode


class Tender(BaseApiTestLogic):

    def __init__(self, *credentials):
        """credentials: user login and password
        tab: competitive or noncompetitive procedures"""
        self.headers = self.set_headers(credentials[0], credentials[1])

    def count_all_records(self, get_tenders_result):
        return get_tenders_result['result']['countAllRecords']

    def get_tenders(self, tab, mode=production_mode, is_real_tenders_for_test_mode=False):
        """method returns dict, also store result to obj attribute - no to use get_tenders"""
        request = post(url=self.base_url + 'api/services/etender/tender/GetTenders',
                       headers=self.headers,
                       data=GetTendersModel(tab, mode, is_real_tenders_for_test_mode).get_request_body())
        assert True is body_to_dict(request.content)['success']
        return body_to_dict(request.content)


class ToDoTenders(Tender):
    def __init__(self, *credentials):
        super().__init__(*credentials)

    def get_tenders_with_responsibles(self, inner_tab):

        obj = GetTendersWithResponsiblesModel()

        if inner_tab == 'in_work':
            obj.set_tenders_in_work_params()

        elif inner_tab == 'archive':
            obj.set_tenders_archive_params()

        elif inner_tab == 'new_tenders':
            pass

        request = post(url=self.base_url + 'api/services/etender/tender/GetTendersWithResponsibles',
                       headers=self.headers,
                       data=obj.get_request_body())
        assert self.check_success_status(body_to_dict(request.content))
        return body_to_dict(request.content)


if __name__ == '__main__':
    pass
