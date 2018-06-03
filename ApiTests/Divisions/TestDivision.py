import json
from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Divisions.Division import Division, DivisionUsersInOrganization


class TestDivisionCRUD(BaseApiTestLogic):

    division = Division()

    def test_get_cookies(self):
        assert self.division.headers.get('Cookie').startswith('ASP.NET_SessionId=')

    def test_get_all_divisions(self):
        """send request with empty JSON data"""
        body = json.dumps({"": ''})
        assert json.loads(self.division.get_division(body)).get('result').get('totalCount') >= 1

    def test_get_divisions_with_paging(self):
        """send request with params, to get first 10 records"""
        body = json.dumps({"Page": 1, "PageSize": 10})
        assert len(json.loads(self.division.get_division(body)).get('result').get('items')) <= 10

    def test_assert_some_division_in_list(self):
        # TODO: remove hardcoded and make parametrize
        old_existing_division = {'id': 38, 'title': 'QA Department'}
        self.division.assert_division_exist(old_existing_division)

    def test_create_division(self):
        self.division.division_for_end_to_end = self.division.create_division('Division_name_api_test')
        self.division.assert_division_exist(self.division.division_for_end_to_end)

    def test_update_division(self):
        new_division_title = 'Updated Department Title with API test'
        result = self.division.update_division(self.division.division_for_end_to_end, new_division_title)
        assert result.get('result').get('title') == new_division_title

    def test_delete_division(self):
        division_before_deletion = self.division.division_for_end_to_end
        self.division.delete_division(division_before_deletion)
        self.division.assert_division_not_exist(division_before_deletion)



class TestAddToDivision(BaseApiTestLogic):

    division_users = DivisionUsersInOrganization()

    def test_add_user_to_division(self):
        """Positive case, if chain already exists - drop it firs"""

        user_id = DivisionUsersInOrganization()._division_head_of_dep_one.get('UserId')
        division = DivisionUsersInOrganization().get_first_division()
        print('\nInput data:', user_id, division)

        print('My data:', self.division_users.get_divisions_with_users())
        # for item in self.division_users.get_divisions_with_users().get('result').get('items'):
        #     if item.get('id') != None:
        #         if 'users' in item and item.get('users') != []:
        #             print('result', item)
        #
        #             print('item.get(users)', item.get('users'))
        #             if division.get('id') in item.get('users'): #and item.get('users').get('id') == user_id:
        #                 print('True')

        # self.division_users.user_division_chain = self.division_users.add_user_to_division(
        #     DivisionUsersInOrganization()._division_head_of_dep_one.get('UserId'),
        #     DivisionUsersInOrganization().get_first_division())

        # print(self.division_users.get_divisions_with_users())

        # if self.division_users.user_division_chain.get('result') == None \
        #         and self.division_users.user_division_chain.get('error').get('message') == \
        #         'User in this division already exist':
        #     self.division_users.delete_user_from_division(
        #         DivisionUsersInOrganization()._division_head_of_dep_one.get('UserId'),
        #         DivisionUsersInOrganization().get_first_division())
        #     self.division_users.user_division_chain = self.division_users.add_user_to_division(
        #         DivisionUsersInOrganization()._division_head_of_dep_one.get('UserId'),
        #         DivisionUsersInOrganization().get_first_division())



        # print('result: ', self.division_users.user_division_chain.get('result'))
        #TODO: add get_chains

    def test_delete_user_from_organization(self):
        request = self.division_users.delete_user_from_division(
            DivisionUsersInOrganization()._division_head_of_dep_one.get('UserId'),
            DivisionUsersInOrganization().get_first_division())

    def test_delete_negative(self):
        pass


    # def test_no_such_division(self, add_user_to_division_parametrized):
    #     print('user: ', add_user_to_division_parametrized.get('userId'))
    #     print(add_user_to_division_parametrized.get('divisionId'))
    #     res = self.division_users.add_user_to_division(add_user_to_division_parametrized.get('userId'),
    #                                              add_user_to_division_parametrized.get('divisionId'))
    #     print('got: ', res)


    # def test_no_such_division(self):
    #     self.add()
    #
    # def test_no_such_user(self):
    #     pass
    #
    # def test_user_already_in_division(self):
    #     pass
    #
    # def test_division_not_in_organization(self):
    #     pass
    #
    # def test_user_not_in_organization(self):
    #     pass
    #
    #
    #
    #
    #

if __name__ == '__main__':
    pass
