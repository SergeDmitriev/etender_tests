import json
from requests import post

from ApiTests.Application.GetTenders import ToDoTenders
from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Helpers import body_to_dict
from ApiTests.app_config import division_admin_login, universal_password


class Division(BaseApiTestLogic):
    division_for_end_to_end = None

    def __init__(self, login=division_admin_login, password=universal_password):
        self.headers = BaseApiTestLogic.set_headers(login, password)

    def get_division(self, body):
        """:returns bytes"""
        request = post(url=self.base_url + 'api/services/etender/division/GetDivisions',
                       headers=self.headers,
                       data=body)
        return request.content

    def assert_division_exist(self, division_obj):
        """Checks, if division in list of dict"""
        # TODO: what to do, if there lots of Divisions?
        assert division_obj in json.loads(self.get_division(self.empty_body_request)).get('result').get('items')

    def assert_division_not_exist(self, division_obj):
        """Checks, if division in list of dict"""
        # TODO: what to do, if there lots of Divisions?
        assert division_obj not in json.loads(self.get_division(self.empty_body_request)).get('result').get('items')

    def create_division(self, division_title):
        """ create obj in Division as dict of (id, title)"""
        request = post(url=self.base_url + 'api/services/etender/division/CreateDivision',
                       headers=self.headers,
                       data=json.dumps({"title": division_title}))
        self.division = json.loads(request.content).get('result')
        print('Created division:', self.division)
        return self.division

    def update_division(self, division, new_title_name):
        print('Before update:', division)
        request = post(url=self.base_url + 'api/services/etender/division/UpdateDivision',
                       headers=self.headers,
                       data=json.dumps({"id": division.get('id'), "title": new_title_name}))

        self.division = json.loads(request.content).get('result')
        print('After update:', self.division)
        return json.loads(request.content)

    def delete_division(self, division):
        """:returns: dict id, title"""
        request = post(url=self.base_url + 'api/services/etender/division/DeleteDivision',
                       headers=self.headers,
                       data=json.dumps({"id": division.get('id')}))
        return request.content

    def add_user_to_division(self, **kwargs):
        """is_head can be 1 or 0"""
        try:
            is_head = kwargs.get('isHead')
        except:
            is_head = 0
        request = post(url=self.base_url + 'api/services/etender/division/AddUserToDivision',
                       headers=self.headers,
                       data=json.dumps({'userid': kwargs.get('user').get('userid'),
                                        'divisionid': kwargs.get('division').get('id'),
                                        'isHead': is_head}))
        print('Adding result: ', json.loads(request.content))
        return json.loads(request.content)

    def delete_user_from_division(self, user, division):
        request = post(url=self.base_url + 'api/services/etender/division/RemoveUserFromDivision',
                       headers=self.headers,
                       data=json.dumps({"userid": user.get('userid'), "divisionid": division.get('id')}))
        print('Deleting result: ', json.loads(request.content))
        return body_to_dict(request.content)

    def update_user_role(self, user_id, division, isHead):
        request = post(url=self.base_url + 'api/services/etender/division/UpdateUserIsHead',
                       headers=self.headers,
                       data=json.dumps({"userid": user_id.get('userid'), "divisionid": division.get('id'),
                                        'isHead': isHead}))
        print('Updating role result: ', json.loads(request.content).get('result'))
        return body_to_dict(request.content)

    def set_responsible_user_tender(self, tender_new_id, user_id, delete_existing_managers=False):
        request = post(url=self.base_url + 'api/services/etender/userTender/SetResponsibleUserTender',
                       headers=self.headers,
                       data=json.dumps({"tenderNewId": tender_new_id,
                                        "userId": user_id,
                                        "deleteExistingManagers": delete_existing_managers}))
        return body_to_dict(request.content)

    def set_responsible_user_tender_list(self, chain_list, delete_existing_managers=False):
        request = post(url=self.base_url + 'api/services/etender/userTender/SetResponsibleUserTenderList',
                       headers=self.headers,
                       data=json.dumps({'list': chain_list, "deleteExistingManagers": delete_existing_managers}))
        return body_to_dict(request.content)

    def return_responsible_user_tender_to_sender(self, tender_new_id, user_id, delete_existing_managers=False):
        request = post(url=self.base_url + 'api/services/etender/userTender/ReturnResponsibleUserTenderToSender',
                       headers=self.headers,
                       data=json.dumps({"tenderNewId": tender_new_id,
                                        "userId": user_id,
                                        "deleteExistingManagers": delete_existing_managers}))
        return body_to_dict(request.content)


class DivisionExts(Division):
    _division_admin = {'userid': '1247', 'Email': 'divisionAdmin@division.com', 'isHead': 0}
    _division_head_of_dep_one = {'userid': '1248', 'Email': 'divisionHeadOfDepOne@division.com', 'isHead': 1}
    _division_head_of_dep_two = {'userid': '1249', 'Email': 'divisionHeadOfDepTwo@division.com', 'isHead': 1}
    _division_head_of_deps_one = {'userid': '1250', 'Email': 'divisionHeadOfDepsOne@division.com', 'isHead': 1}
    _division_head_of_deps_two = {'userid': '1251', 'Email': 'divisionHeadOfDepsTwo@division.com', 'isHead': 1}
    _division_manager_one = {'userid': '1252', 'Email': 'divisionManagerOne@division.com', 'isHead': 0}
    _division_manager_two = {'userid': '1253', 'Email': 'divisionManagerTwo@division.com', 'isHead': 0}
    _division_manager_three = {'userid': '1254', 'Email': 'divisionManagerThree@division.com', 'isHead': 0}
    _division_manager_four = {'userid': '1255', 'Email': 'divisionManagerFour@division.com', 'isHead': 0}
    _unassigned_user_to_division = {'userid': '1266', 'Email': 'UnassignedUserToDivision@division.com', 'isHead': 0}

    def __init__(self, *kwargs):
        super().__init__(*kwargs)

    def check_isHead(self, response):
        res = response.get('result').get('isHead')
        if res == 1:
            return True
        else:
            return False

    def get_exact_division(self, division_number=0):
        """:returns first division from current organization in dict
        sample: {'id': 1, 'title': 'Support Department'}"""
        return json.loads(self.get_division(self.empty_body_request)).get('result').get('items')[division_number]

    def group_user_and_division_into_chain(self, **kwargs):
        """input data: user=, division="""
        chain = {'userid': int(kwargs.get('user').get('userid')),
                 'divisionid': kwargs.get('division').get('id')}
        print('Chain is: ', chain)
        return chain

    def get_divisions_with_users(self, body=json.dumps({"": ''})):
        request = post(url=self.base_url + 'api/services/etender/division/GetDivisionsWithUsers',
                       headers=self.headers,
                       data=body)
        return json.loads(request.content)

    def get_all_user_division_chains(self, show_isHead=False):
        """ return list of dict with keys userid, divisionid
        returns also role, if isHead=1"""
        obj = self.get_divisions_with_users()
        one_chain = {}
        users_in_divisions = []

        if obj.get('success') and obj.get('error') is None:
            for division in obj.get('result').get('items'):  # division - дивижн с вложенными юзерами
                if division.get('users') != [] and division.get('id') is not None:
                    try:
                        for user in division.get('users'):
                            one_chain['userid'] = user.get('id')
                            one_chain['divisionid'] = division.get('id')
                            if show_isHead:
                                one_chain['divisionid'] = division.get('isHead')

                                users_in_divisions.append({'userid': user.get('id'),
                                                           'divisionid': division.get('id'),
                                                           'isHead': user.get('isHead')})
                            else:
                                users_in_divisions.append({'userid': user.get('id'),
                                                           'divisionid': division.get('id')})
                    except Exception as e:
                        print(e)
        return users_in_divisions

    def delete_user_from_all_divisions(self, user, chains_to_delete):
        """chains_to_delete - dict like {'userid': 1250, 'divisionid': 1, 'isHead': True}"""
        for i in chains_to_delete:
            try:
                i['id'] = i.pop('divisionid')
                self.delete_user_from_division(user, i)
            except KeyError:
                self.delete_user_from_division(user, i)

    def find_user_in_divisions(self, user_to_check, list_of_chains):
        """ return list of dicts like {'userid': 1250, 'divisionid': 1, 'isHead': True}"""
        count = 0
        chains = []

        for i in list_of_chains:
            x = i.get('userid')
            if int(user_to_check.get('userid')) == x:
                chains.append({'userid': i.get('userid'), 'divisionid': i.get('divisionid')})
                count += 1
            else:
                pass
        return chains

    def check_if_chain_exist(self, chain):
        """chain should be dict {userid, divisionid}"""
        user_division_chain = chain
        list_of_chains = self.get_all_user_division_chains()
        res = False

        try:
            # Check, if our chain already exists
            assert user_division_chain in list_of_chains
            res = True
        except AssertionError:
            print('Chain doesnt exist')
        finally:
            return res

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

    def assure_tender_list_assigned_to_user(self, assignment_result, tender_user_chains):
        """tender_user_chains: [{'tenderNewId': 'xxx', 'userId': '1247'},...}]"""
        c = 0
        result = None
        chains_count = len(tender_user_chains)
        try:
            l = assignment_result['result']['list']
            result = 'tender_list'
        except TypeError:
            pass

        try:
            l = assignment_result['error']['message']
            result = 'permission denied'
        except (KeyError, TypeError):
            pass

        if result == 'tender_list':
            for i in assignment_result['result']['list']:
                for j in tender_user_chains:
                    if i['tenderNewId'] == j['tenderNewId'] and (i['userId']) == int(j['userId']):
                        c += 1
                    else:
                        pass
            if chains_count == c:
                return True
            else:
                return False
        elif result == 'permission denied':
            return False
        else:
            raise AssertionError

    def group_tender_and_user_into_chain_list(self, list_of_tender_new_ids, user_id):
        chain_list = []
        for tender in list_of_tender_new_ids:
            chain_list.append({'tenderNewId': tender, 'userId': user_id})
        return chain_list


if __name__ == '__main__':
    pass
