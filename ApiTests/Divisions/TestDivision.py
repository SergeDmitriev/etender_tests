import json
from ApiTests.Divisions.Division import Division, CreateDivision, UpdateDivision, DeleteDivision, \
    AddUserToDivision


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
        old_existing_division = {'id': 38, 'title': 'QA Department'}
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
        division_before_deletion = self.division
        self.delete_division(self.division)
        self.assert_division_not_exist(division_before_deletion)



class TestAddUserToDivision(AddUserToDivision):


    def AddUserToDivision(self):
        temp_division = CreateDivision.precondition_create_division('Division created for joining user').get('id')
        print('created obj', temp_division)
        self.add(1248, temp_division)
        # get list of divisions


    def test_no_such_division(self):
        self.add()

    def test_no_such_user(self):
        pass

    def test_user_already_in_division(self):
        pass

    def test_division_not_in_organization(self):
        pass

    def test_user_not_in_organization(self):
        pass






if __name__ == '__main__':
    pass
