from requests import post

from ApiTests.Application.Models.GetTendersModel import GetTendersModel, GetTendersWithResponsiblesModel
from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Helpers import body_to_dict, page_switch_times
from ApiTests.app_config import production_mode, universal_password, division_admin_login


class Tender(BaseApiTestLogic):

    def __init__(self, *credentials):
        """credentials: user login and password
        tab: competitive or noncompetitive procedures"""
        self.headers = self.set_headers(credentials[0], credentials[1])

    def get_tenders(self, tab, mode=production_mode, is_real_tenders_for_test_mode=False, page_number=1):
        """method returns dict, also store result to obj attribute - no to use get_tenders"""
        request = post(url=self.base_url + 'api/services/etender/tender/GetTenders',
                       headers=self.headers,
                       data=GetTendersModel(tab, mode, is_real_tenders_for_test_mode,
                                            page_number=page_number).get_request_body())
        assert True is body_to_dict(request.content)['success']
        return body_to_dict(request.content)

    def count_all_records(self, get_tenders_result):
        return get_tenders_result['result']['countAllRecords']


class ToDoTenders(Tender):
    def __init__(self, *credentials):
        super().__init__(*credentials)

    def get_tenders_with_responsibles(self, inner_tab, page_number=1):

        obj = GetTendersWithResponsiblesModel(page_number=page_number)

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

    def get_all_assigned_users_for_tenders(self, get_tenders_result):
        """get chain {tender_new_id, }"""
        chains = []

        for i in page_switch_times(self.count_all_records(get_tenders_result)):
            result_from_page = self.get_tenders_with_responsibles(inner_tab='in_work', page_number=i)
            for x in result_from_page['result']['tender']:
                chains.append({'tender_new_id': x['id'],
                               'responsibles': x['responsibles']
                               })
        return chains

    def get_top_100_tender_ids(self):
        """get tenders from 10 pages in new_tenders tab"""
        tenders_id = []
        for i in page_switch_times(100):
            result_from_page = self.get_tenders_with_responsibles(inner_tab='new_tenders', page_number=i)
            for x in result_from_page['result']['tender']:
                tenders_id.append({'tender_new_id': x['id']})
        return tenders_id

    def get_list_unassigned_tender(self, all_assigned_tenders_for_user_chain, tender_id_list_to_check):
        """input: all_assigned_tenders_for_user_chain - {'tender_new_id': '', 'responsibles': [{}]'
        tender_id_list_to_check - {'tender_new_id': ''...}"""
        result_ids = []
        a = [i['tender_new_id'] for i in all_assigned_tenders_for_user_chain]
        b = [i['tender_new_id'] for i in tender_id_list_to_check]

        # same result:
        # return list(filter(lambda x: x not in [i['tender_new_id'] for i in all_assigned_tenders_for_user_chain],
        # [i['tender_new_id'] for i in tender_id_list_to_check]))

        for i in b:
            if i not in a:
                result_ids.append(i)
        return result_ids

    def assure_tender_assigned_to_user(self, tender_new_id, assigned_user):
        """method returns None, if user not assigned for tender"""
        tenders_from_admin = ToDoTenders(division_admin_login, universal_password)  # only admin see all chains

        all_tender_id_responsibles_chains = tenders_from_admin.get_all_assigned_users_for_tenders(
            tenders_from_admin.get_tenders_with_responsibles('in_work'))

        for chain in all_tender_id_responsibles_chains:
            if chain['tender_new_id'] == tender_new_id:
                for res in chain['responsibles']:
                    if res['emailAddress'] == assigned_user:
                        return True
            else:
                pass


if __name__ == '__main__':
    pass
