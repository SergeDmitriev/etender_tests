import json
from requests import post
from ApiTests.BaseApiTestLogic import BaseApiTestLogic, set_headers_function


class Division(BaseApiTestLogic):

    division_for_end_to_end = None

    def get_division(self, body):
        """:returns bytes"""
        request = post(url=self.base_url + 'api/services/etender/division/GetDivisions',
                       headers=self.set_headers(),
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

    # def get_divisions_with_users(self):
    #     pass

    def create_division(self, division_title):
        """ create obj in Division as dict of (id, title)"""
        request = post(url=self.base_url + 'api/services/etender/division/CreateDivision',
                       headers=self.set_headers(),
                       data=json.dumps({"title": division_title}))
        self.division = json.loads(request.content).get('result')
        print('Created division:', self.division)
        return self.division

#
#     @staticmethod
#     def precondition_create_division(division_title):
#         """:returns dict of id, title"""
#         request_create = post(url=base_prozorro_url + 'api/services/etender/division/CreateDivision',
#                               headers=set_headers_function(),
#                               data=json.dumps({"title": division_title}))
#         return json.loads(request_create.content).get('result')


    def update_division(self, division, new_title_name):
        print('Before update:', division)
        request = post(url=self.base_url + 'api/services/etender/division/UpdateDivision',
                       headers=self.set_headers(),
                       data = json.dumps({"id": division.get('id'), "title": new_title_name}))
        self.division = json.loads(request.content).get('result')
        print('After update:', self.division)
        return json.loads(request.content)

    def delete_division(self, division):
        """:returns: dict id, title"""
        request = post(url=self.base_url + 'api/services/etender/division/DeleteDivision',
                       headers=self.set_headers(),
                       data = json.dumps({"id": division.get('id')}))
        return request.content


# class AddUserToDivision(Division):
#
#     @staticmethod
#     def add(user_id, division_id):
#         request_add_user_to_division = post(url=base_prozorro_url + 'api/services/etender/division/AddUserToDivision',
#                               headers=set_headers_function(),
#                               data=json.dumps({"userId": user_id, "divisionId": division_id.get('id')}))
#         print('result of adding: ',json.loads(request_add_user_to_division.content))
#         return json.loads(request_add_user_to_division.content)
#
#
#     def delete_temp_division(self, division):
#         request = post(url=base_prozorro_url + 'api/services/etender/division/DeleteDivision',
#                        headers=set_headers_function(),
#                        data=json.dumps({"id": division.get('id')}))
#         return request.content
#
