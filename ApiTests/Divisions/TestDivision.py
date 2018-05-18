import json
import pytest
from requests import post
from ApiTests.BaseApiTestLogic import BaseApiTestLogic


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
        assert division_obj in json.loads(cls.get_division(body)).get('result').get('items')


class CreateDivision(Division):

    @classmethod
    def create_division(cls, division_title):
        """: create obj in Division as dict of (id, title)"""
        request = post(url=cls.base_url + 'api/services/etender/division/CreateDivision',
                       headers=cls.set_headers(),
                       data=json.dumps({"title": division_title}))
        Division.division = json.loads(request.content).get('result')
        print('Created division:', Division.division)


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
        request = post(url=cls.base_url + 'api/services/etender/division/DeleteDivision',
                       headers=cls.set_headers(),
                       data = json.dumps({"id": division.get('id')}))
        return request.content


class TestGetDivisions(Division):
    """Get Division by Id impossible"""

    def test_get_cookies(self):
        print(self.get_cookies())
        assert self.get_cookies().startswith('ASP.NET_SessionId=')

    def test_get_all_divisions(self):
        """send request with empty JSON data"""
        body = json.dumps({"": ''})
        assert json.loads(self.get_division(body)).get('result').get('totalCount') >= 1

    def test_get_divisions_with_paging(self):
        """send request with params, to get first 10 records"""
        body = json.dumps({"Page": 1, "PageSize": 10})
        assert len(json.loads(self.get_division(body)).get('result').get('items')) <= 10

    def test_assert_division_in_list(self):
        # TODO: remove hardcoded and make parametrize
        old_existing_division = {'id': 39, 'title': 'Develop Department'}
        self.assert_division_exist(old_existing_division)


class TestCreateDivision(CreateDivision):

    def test_create_division(self):
        self.create_division('Division_name_api_test')
        self.assert_division_exist(self.division)


class TestUpdateDivision(UpdateDivision):

    def test_update_division(self):
        new_division_title = 'Updated Department Title with API test'
        result = self.update_division(self.division, new_division_title)
        assert result.get('result').get('title') == new_division_title


class TestDeleteDivision(DeleteDivision):

    def test_delete_division(self):
        self.delete_division(self.division)
        print(self.delete_division(self.division))

    def test_assert_division_not_in_list(self):
        # TODO: remove hardcoded and make parametrize
        old_existing_division = {'id': 39, 'title': 'Develop Department'}
        self.assert_division_exist(old_existing_division)


if __name__ == '__main__':
    pass



