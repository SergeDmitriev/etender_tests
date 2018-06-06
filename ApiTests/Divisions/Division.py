import json
from requests import post
from ApiTests.BaseApiTestLogic import BaseApiTestLogic, set_headers_function


class Division(BaseApiTestLogic):

    division_for_end_to_end = None
    headers = BaseApiTestLogic.set_headers()

    def get_division(self, body):
        """:returns bytes"""
        request = post(url=self.base_url + 'api/services/etender/division/GetDivisions',
                       headers=self.headers,
                       data=body)
        return request.content

    def assert_division_exist(self, division_obj):
        """Checks, if division in list of dict"""
        # TODO: what to do, if there lots of Divisions?
        body = json.dumps({"": ''})
        assert division_obj in json.loads(self.get_division(body)).get('result').get('items')

    def assert_division_not_exist(self, division_obj):
        """Checks, if division in list of dict"""
        # TODO: what to do, if there lots of Divisions?
        body = json.dumps({"": ''})
        assert division_obj not in json.loads(self.get_division(body)).get('result').get('items')

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
                       data = json.dumps({"id": division.get('id'), "title": new_title_name}))
        self.division = json.loads(request.content).get('result')
        print('After update:', self.division)
        return json.loads(request.content)

    def delete_division(self, division):
        """:returns: dict id, title"""
        request = post(url=self.base_url + 'api/services/etender/division/DeleteDivision',
                       headers=self.headers,
                       data = json.dumps({"id": division.get('id')}))
        return request.content

    def add_user_to_division(self, user_id, division):
        request = post(url=self.base_url + 'api/services/etender/division/AddUserToDivision',
                              headers=self.headers,
                              data=json.dumps({"userId": user_id, "divisionId": division.get('id')}))
        print('Adding result: ',json.loads(request.content))
        return json.loads(request.content)

    def delete_user_from_division(self, user_id, division):
        request = post(url=self.base_url + 'api/services/etender/division/RemoveUserFromDivision',
                       headers=self.headers,
                       data=json.dumps({"userId": user_id, "divisionId": division.get('id')}))
        print('Deleting result: ', json.loads(request.content))
        return json.loads(request.content)

    def get_divisions_with_users(self, body=json.dumps({"": ''})):
        request = post(url=self.base_url + 'api/services/etender/division/GetDivisionsWithUsers',
                       headers=self.headers,
                       data=body)
        return json.loads(request.content)

    def get_user_division_chain(self):
        """:returns list of dict with keys userid, divisionid"""
        obj = self.get_divisions_with_users()
        one_chain = {}
        users_in_divisions = []

        if obj.get('success') and obj.get('error') is None:
            for item in obj.get('result').get('items'):     #item - дивижн с вложенными юзерами
                if item.get('users') != [] and item.get('id') is not None:
                    try:
                        for i in item.get('users'):
                            one_chain['userid'] = i.get('id')
                            one_chain['divisionid'] = item.get('id')
                            users_in_divisions.append({'userid': i.get('id'), 'divisionid': item.get('id')})
                            # users_in_divisions.append(one_chain)
                    except Exception as e:
                        print(e)
        return users_in_divisions

    def check_if_chain_exist(self, userid_divisionid):
        user_division_chain = userid_divisionid
        list_of_chains = self.get_user_division_chain()
        res = False

        try:
            # Check, if our chain already exists
            assert user_division_chain in list_of_chains
            res = True
        except AssertionError as e:
            print('User not in chain')
        finally:
            return res


class DivisionUsersInOrganization(Division):

    def __init__(self):
        self._division_admin = {'UserId': '1247', 'Email': 'divisionAdmin@division.com'}
        self._division_head_of_dep_one = {'UserId': '1248', 'Email': 'divisionHeadOfDepOne@division.com'}
        self._division_head_of_dep_two = {'UserId': '1249', 'Email': 'divisionHeadOfDepTwo@division.com'}
        self._division_head_of_deps_one = {'UserId': '1250', 'Email': 'divisionHeadOfDepsOne@division.com'}
        self._division_head_of_deps_two = {'UserId': '1251', 'Email': 'divisionHeadOfDepsTwo@division.com'}
        self._division_manager_one = {'UserId': '1252', 'Email': 'divisionManagerOne@division.com'}
        self._division_manager_two = {'UserId': '1253', 'Email': 'divisionManagerTwo@division.com'}
        self._division_manager_three = {'UserId': '1254', 'Email': 'divisionManagerThree@division.com'}
        self._division_manager_four = {'UserId': '1255', 'Email': 'divisionManagerFour@division.com'}
        self._unassigned_user_to_division = {'UserId': '1266', 'Email': 'UnassignedUserToDivision@division.com'}

    def get_first_division(self):
        """:returns first division from current organization in dict"""
        body = json.dumps({"": ''})
        return json.loads(self.get_division(body)).get('result').get('items')[0]


    def get_users_in_division(self):
        pass


if __name__ == '__main':
    pass
