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
        old_existing_division = {'id': 40, 'title': 'Support Department'}
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
    # TODO: add preconditions
    chains = DivisionUsersInOrganization()

    user_div = chains.group_user_and_division(
        chains._division_head_of_dep_one.get('UserId'),
        chains.get_first_division().get('id'))

    def test_add_user_to_division(self):
        """Positive case, if chain already exists - drop it firs"""
        if self.chains.check_if_chain_exist(self.user_div):
            # Delete user_division chain from DB
            self.chains.delete_user_from_division(
                self.chains._division_head_of_dep_one.get('UserId'),
                self.chains.get_first_division())
            assert self.chains.check_if_chain_exist(self.user_div) is False

        self.chains.user_division_chain = self.chains.add_user_to_division(
            self.chains._division_head_of_dep_one.get('UserId'),
            self.chains.get_first_division())
        assert self.chains.check_if_chain_exist(self.user_div)

    def test_add_nonexistent_user_to_division(self):
        all_chains = self.chains.get_user_division_chain()
        user_to_add = {'UserId': '0', 'Email': 'nonexistentUser@division.com'}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user_to_add.get('UserId'),
            self.chains.get_first_division())

        assert user_to_add not in all_chains and \
               self.chains.user_division_chain.get('error').get('message') \
               == 'You in different organization with user try to add'

    def test_add_user_to_nonexistent_division(self):
        all_chains = self.chains.get_user_division_chain()
        user_to_add = self.chains._unassigned_user_to_division
        nonexistent_division = {'id': 0, 'title': 'Nonexistent division'}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user_to_add.get('UserId'), nonexistent_division)

        assert self.chains.group_user_and_division(user_to_add.get('UserId'), nonexistent_division) \
               not in all_chains and \
               'Підрозділ не в вашій організації' == \
               self.chains.user_division_chain.get('error').get('message')

    def test_add_user_if_chain_exists(self):
        if not self.chains.check_if_chain_exist(self.user_div):
            self.chains.user_division_chain = self.chains.add_user_to_division(
                self.chains._division_head_of_dep_one.get('UserId'),
                self.chains.get_first_division())
            assert self.chains.check_if_chain_exist(self.user_div)

        self.chains.user_division_chain = self.chains.add_user_to_division(
            self.chains._division_head_of_dep_one.get('UserId'),
            self.chains.get_first_division())

        assert 'User in this division already exist' == \
               self.chains.user_division_chain.get('error').get('message')

        self.chains.delete_user_from_division(
            self.chains._division_head_of_dep_one.get('UserId'),
            self.chains.get_first_division())
        assert self.chains.check_if_chain_exist(self.user_div) is False

    def test_add_user_to_foreign_division(self):
        all_chains = self.chains.get_user_division_chain()
        #TODO: all_chains can be None! create preconditions
        user_to_add = self.chains._unassigned_user_to_division
        foreign_division = {'id': 35, 'title': 'test'}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user_to_add.get('UserId'), foreign_division)

        assert self.chains.group_user_and_division(user_to_add.get('UserId'), foreign_division) \
               not in all_chains and \
               'Підрозділ не в вашій організації' == self.chains.user_division_chain.get('error').get('message')

    def test_add_foreign_user_to_division(self):
        all_chains = self.chains.get_user_division_chain()
        #TODO remove hardcore
        user_to_add = {'UserId': '1', 'Email': 'not_my_user@test.com'}
        division = self.chains.get_first_division()

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user_to_add.get('UserId'), division)

        assert 'You in different organization with user try to add' == \
               self.chains.user_division_chain.get('error').get('message')
        assert user_to_add not in all_chains


class TestDeleteFromDivision(BaseApiTestLogic):
    # TODO: add preconditions
    chains = DivisionUsersInOrganization()

    user_div = chains.group_user_and_division(
        chains._division_head_of_dep_one.get('UserId'),
        chains.get_first_division().get('id'))

    def test_delete_user_from_division(self):
        if not self.chains.check_if_chain_exist(self.user_div):
            # Add user:
            self.chains.user_division_chain = self.chains.add_user_to_division(
                self.chains._division_head_of_dep_one.get('UserId'),
                self.chains.get_first_division())
            assert self.chains.check_if_chain_exist(self.user_div)

        self.chains.delete_user_from_division(
            self.chains._division_head_of_dep_one.get('UserId'),
            self.chains.get_first_division())
        assert self.chains.check_if_chain_exist(self.user_div) is False

    def test_delete_user_from_nonexistent_division(self):
        pass

    def test_delete_nonexistent_user_from_division(self):
        pass

    def test_delete_nonexistent_chain(self):
        pass

    def test_delete_user_from_foreign_division(self):
        pass

    def test_delete_foreign_user_from_division(self):
        pass

if __name__ == '__main__':
    pass
