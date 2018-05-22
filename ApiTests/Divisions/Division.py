import json
from requests import post
from ApiTests.BaseApiTestLogic import BaseApiTestLogic, set_headers_function
from ApiTests.etender_data_api import base_prozorro_url


class Division(BaseApiTestLogic):
    division = None

    @classmethod
    def get_division(cls, body):
        """:returns bytes"""
        request = post(url=cls.base_url + 'api/services/etender/division/GetDivisions',
                       headers=cls.set_headers(),
                       data=body)
        return request.content

    @classmethod
    def assert_division_exist(cls, division_obj):
        """Checks, if division in list of dict"""
        # TODO: what to do, if there lots of Divisions?
        body = json.dumps({"": ''})
        assert division_obj in json.loads(cls.get_division(body)).get('result').get('items')

    @classmethod
    def assert_division_not_exist(cls, division_obj):
        """Checks, if division in list of dict"""
        # TODO: what to do, if there lots of Divisions?
        body = json.dumps({"": ''})
        assert division_obj not in json.loads(cls.get_division(body)).get('result').get('items')

    @classmethod
    def get_divisions_with_users(cls):
        pass


class CreateDivision(Division):

    @classmethod
    def create_division(cls, division_title):
        """ create obj in Division as dict of (id, title)"""
        request = post(url=cls.base_url + 'api/services/etender/division/CreateDivision',
                       headers=cls.set_headers(),
                       data=json.dumps({"title": division_title}))
        Division.division = json.loads(request.content).get('result')
        print('Created division:', Division.division)

    @staticmethod
    def precondition_create_division(division_title):
        """:returns dict of id, title"""
        request_create = post(url=base_prozorro_url + 'api/services/etender/division/CreateDivision',
                              headers=set_headers_function(),
                              data=json.dumps({"title": division_title}))
        return json.loads(request_create.content).get('result')


class UpdateDivision(Division):

    @classmethod
    def update_division(cls, division, new_title_name):
        print('Before update:', division)
        request = post(url=cls.base_url + 'api/services/etender/division/UpdateDivision',
                       headers=cls.set_headers(),
                       data = json.dumps({"id": division.get('id'), "title": new_title_name}))
        Division.division = json.loads(request.content).get('result')
        print('After update:', Division.division)
        return json.loads(request.content)


class DeleteDivision(Division):

    @classmethod
    def delete_division(cls, division):
        """:returns: dict id, title"""
        request = post(url=cls.base_url + 'api/services/etender/division/DeleteDivision',
                       headers=cls.set_headers(),
                       data = json.dumps({"id": division.get('id')}))
        return request.content


class AddUserToDivision(Division):

    @staticmethod
    def add(user_id, division_id):
        request_add_user_to_division = post(url=base_prozorro_url + 'api/services/etender/division/AddUserToDivision',
                              headers=set_headers_function(),
                              data=json.dumps({"userId": user_id, "divisionId": division_id.get('id')}))
        print('result of adding: ',json.loads(request_add_user_to_division.content))
        return json.loads(request_add_user_to_division.content)


    def delete_temp_division(self, division):
        request = post(url=base_prozorro_url + 'api/services/etender/division/DeleteDivision',
                       headers=set_headers_function(),
                       data=json.dumps({"id": division.get('id')}))
        return request.content

