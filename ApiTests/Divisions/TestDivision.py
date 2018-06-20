import json
from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Divisions.Division import Division, DivisionUserChain


class TestDivisionCRUD(BaseApiTestLogic):

    division = Division()

    def test_get_cookies(self):
        # TODO: GetDivision method called while init
        assert self.division.headers.get('Cookie').startswith('ASP.NET_SessionId=')

    def test_get_all_divisions(self):
        """send request with empty JSON data"""
        assert json.loads(self.division.get_division(self.empty_body_request)).get('result').get('totalCount') >= 1

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


class TestAddHeadToDivision(BaseApiTestLogic):
    # Add manager to division
    # TODO: много одинакового кода
    chains = DivisionUserChain()

    user_div = chains.group_user_and_division_into_chain(
        user=chains._division_head_of_dep_one,
        division=chains.get_first_division())

    def test_add_user_to_division_as_head(self):
        """Positive case, if chain already exists - drop it first
        Parameter isHead not sent while adding to division"""
        user = self.chains.group_user_and_division_into_chain(
        user=self.chains._division_head_of_dep_one,
        division=self.chains.get_first_division())

        if self.chains.check_if_chain_exist(user):
            # Delete user_division chain from DB
            self.chains.delete_user_from_division(
                self.chains._division_head_of_dep_one.get('UserId'),
                self.chains.get_first_division())
            assert self.chains.check_if_chain_exist(user) is False

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=self.chains._division_head_of_dep_one,
            division=self.chains.get_first_division(),
            isHead=1)
        assert self.chains.check_if_chain_exist(user)
        assert True == self.chains.check_isHead(self.chains.user_division_chain)

    def test_add_nonexistent_user_to_division_as_head(self):
        all_chains = self.chains.get_user_division_chain()
        user_to_add = {'UserId': '0', 'Email': 'nonexistentUser@division.com', 'isHead': 1}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=self.chains.get_first_division(),
            isHead=1)

        assert user_to_add not in all_chains and \
               self.chains.user_division_chain.get('error').get('message') \
               == 'You in different organization with user try to add'

    def test_add_user_to_nonexistent_division_as_head(self):
        all_chains = self.chains.get_user_division_chain()
        user_to_add = self.chains._unassigned_user_to_division
        nonexistent_division = {'id': 0, 'title': 'Nonexistent division', 'isHead': 1}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=nonexistent_division,
            isHead=1)

        assert self.chains.group_user_and_division_into_chain(
            user=user_to_add,
            division=nonexistent_division) \
               not in all_chains and \
               'Підрозділ не в вашій організації' == \
               self.chains.user_division_chain.get('error').get('message')

    def test_add_user_if_chain_exists_as_head(self):
        if not self.chains.check_if_chain_exist(self.user_div):
            self.chains.user_division_chain = self.chains.add_user_to_division(
                user=self.chains._division_head_of_dep_one,
                division=self.chains.get_first_division(),
                isHead=1)
            assert self.chains.check_if_chain_exist(self.user_div)
            assert True == self.chains.check_isHead(self.chains.user_division_chain)

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=self.chains._division_head_of_dep_one,
            division=self.chains.get_first_division(),
            isHead=1)

        assert 'User in this division already exist' == \
               self.chains.user_division_chain.get('error').get('message')

        self.chains.delete_user_from_division(
            self.chains._division_head_of_dep_one.get('UserId'),
            self.chains.get_first_division())
        assert self.chains.check_if_chain_exist(self.user_div) is False

    def test_add_user_to_foreign_division_as_head(self):
        all_chains = self.chains.get_user_division_chain()
        #TODO: all_chains can be None! create preconditions
        user_to_add = self.chains._unassigned_user_to_division
        foreign_division = {'id': 35, 'title': 'test', 'isHead':1}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=foreign_division,
            isHead=1)

        assert self.chains.group_user_and_division_into_chain(
            user=user_to_add, division=foreign_division) \
               not in all_chains and \
               'Підрозділ не в вашій організації' == self.chains.user_division_chain.get('error').get('message')

    def test_add_foreign_user_to_division_as_head(self):
        all_chains = self.chains.get_user_division_chain()
        #TODO remove hardcore
        user_to_add = {'UserId': '1', 'Email': 'not_my_user@test.com', 'isHead':1}
        division = self.chains.get_first_division()

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=division,
            isHead=1)

        assert 'You in different organization with user try to add' == \
               self.chains.user_division_chain.get('error').get('message')
        assert user_to_add not in all_chains


class TestAddManagerToDivision(BaseApiTestLogic):
    # Add manager to division
    # TODO: много одинакового кода
    chains = DivisionUserChain()

    user_div = chains.group_user_and_division_into_chain(
        user=chains._division_manager_one,
        division=chains.get_first_division())

    def test_add_user_to_division_as_manager(self):
        """Positive case, if chain already exists - drop it first
        isHead = null"""
        user = self.chains.group_user_and_division_into_chain(
            user=self.chains._division_manager_one,
            division=self.chains.get_first_division())

        if self.chains.check_if_chain_exist(user):
            # Delete user_division chain from DB
            self.chains.delete_user_from_division(
                self.chains._division_manager_one.get('UserId'),
                self.chains.get_first_division())
            assert self.chains.check_if_chain_exist(user) is False

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=self.chains._division_manager_one,
            division=self.chains.get_first_division())
        assert self.chains.check_if_chain_exist(user)
        assert False == self.chains.check_isHead(self.chains.user_division_chain)

    def test_add_nonexistent_user_to_division_as_manager(self):
        all_chains = self.chains.get_user_division_chain()
        user_to_add = {'UserId': '0', 'Email': 'nonexistentUser@division.com'}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=self.chains.get_first_division())

        assert user_to_add not in all_chains and \
               self.chains.user_division_chain.get('error').get('message') \
               == 'You in different organization with user try to add'

    def test_add_user_to_nonexistent_division_as_manager(self):
        all_chains = self.chains.get_user_division_chain()
        user_to_add = self.chains._division_manager_one
        nonexistent_division = {'id': 0, 'title': 'Nonexistent division'}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=nonexistent_division)

        assert self.chains.group_user_and_division_into_chain(
            user=user_to_add,
            division=nonexistent_division) \
               not in all_chains and \
               'Підрозділ не в вашій організації' == \
               self.chains.user_division_chain.get('error').get('message')

    def test_add_user_if_chain_exists_as_manager(self):
        if not self.chains.check_if_chain_exist(self.user_div):
            self.chains.user_division_chain = self.chains.add_user_to_division(
                user=self.chains._division_manager_one,
                division=self.chains.get_first_division())
            assert self.chains.check_if_chain_exist(self.user_div)

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=self.chains._division_manager_one,
            division=self.chains.get_first_division())

        assert 'User in this division already exist' == \
               self.chains.user_division_chain.get('error').get('message')

        self.chains.delete_user_from_division(
            self.chains._division_manager_one.get('UserId'),
            self.chains.get_first_division())
        assert self.chains.check_if_chain_exist(self.user_div) is False

    def test_add_user_to_foreign_division_as_manager(self):
        all_chains = self.chains.get_user_division_chain()
        #TODO: all_chains can be None! create preconditions
        user_to_add = self.chains._division_manager_one
        foreign_division = {'id': 35, 'title': 'test'}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=foreign_division)

        assert self.chains.group_user_and_division_into_chain(
            user=user_to_add, division=foreign_division) \
               not in all_chains and \
               'Підрозділ не в вашій організації' == self.chains.user_division_chain.get('error').get('message')

    def test_add_foreign_user_to_division_as_manager(self):
        all_chains = self.chains.get_user_division_chain()
        #TODO remove hardcore
        user_to_add = {'UserId': '1', 'Email': 'not_my_user@test.com'}
        division = self.chains.get_first_division()

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=division)

        assert 'You in different organization with user try to add' == \
               self.chains.user_division_chain.get('error').get('message')
        assert user_to_add not in all_chains


class TestDeleteFromDivision(BaseApiTestLogic):
    # TODO: add preconditions, maybe parametrize
    chains = DivisionUserChain()
# user - head of division
    def test_delete_user_from_division(self):
        user_div = self.chains.group_user_and_division_into_chain(
            user=self.chains._division_head_of_dep_one,
            division=self.chains.get_first_division())

        # TODO: make precondition "if chain not exist - create it"
        if not self.chains.check_if_chain_exist(user_div):
            # Add user:
            self.chains.user_division_chain = self.chains.add_user_to_division(
                user=self.chains._division_head_of_dep_one,
                division=self.chains.get_first_division())
            assert self.chains.check_if_chain_exist(user_div)

        self.chains.delete_user_from_division(
            self.chains._division_head_of_dep_one.get('UserId'),
            self.chains.get_first_division())
        assert self.chains.check_if_chain_exist(user_div) is False

    def test_delete_user_from_nonexistent_division(self):

        nonexistent_division = {'id': 0, 'title': 'Nonexistent division'}

        chain = self.chains.group_user_and_division_into_chain(
            user=self.chains._division_head_of_dep_one,
            division=nonexistent_division)

        result = self.chains.delete_user_from_division(
            self.chains._division_head_of_dep_one.get('UserId'),
            nonexistent_division)

        assert self.chains.check_if_chain_exist(chain) is False
        assert 'Підрозділ не в вашій організації' == result.get('error').get('message')

    def test_delete_nonexistent_user_from_division(self):
        # TODO: test fails now
        user_to_delete = {'UserId': '0', 'Email': 'nonexistentUser@division.com'}

        chain = self.chains.group_user_and_division_into_chain(
            user=user_to_delete,
            division=self.chains.get_first_division())

        result = self.chains.delete_user_from_division(
            user_to_delete.get('UserId'),
            self.chains.get_first_division())

        assert self.chains.check_if_chain_exist(chain) is False
        assert 'Підрозділ не в вашій організації' == result.get('error').get('message')

    def test_delete_nonexistent_chain(self):
        user_to_delete = {'UserId': '0', 'Email': 'nonexistentUser@division.com'}
        nonexistent_division = {'id': 0, 'title': 'Nonexistent division'}

        chain = self.chains.group_user_and_division_into_chain(
            user=user_to_delete,
            division=nonexistent_division)

        result = self.chains.delete_user_from_division(
            user_to_delete.get('UserId'),
            nonexistent_division)

        assert self.chains.check_if_chain_exist(chain) is False
        assert 'Підрозділ не в вашій організації' == result.get('error').get('message')

    def test_delete_user_from_foreign_division(self):
        user_to_delete = {'UserId': '0', 'Email': 'nonexistentUser@division.com'}
        foreign_division = {'id': 35, 'title': 'test'}

        chain = self.chains.group_user_and_division_into_chain(
            user=self.chains._division_head_of_dep_one,
            division=foreign_division)

        result = self.chains.delete_user_from_division(
            user_to_delete.get('UserId'),
            foreign_division)

        assert self.chains.check_if_chain_exist(chain) is False
        assert 'Підрозділ не в вашій організації' == result.get('error').get('message')

    def test_delete_foreign_user_from_division(self):
        user_to_delete = {'UserId': '235', 'Email': 'turkobubro@meta.ua'}

        chain = self.chains.group_user_and_division_into_chain(
            user=self.chains._division_head_of_dep_one,
            division=self.chains.get_first_division())

        result = self.chains.delete_user_from_division(
            user_to_delete.get('UserId'),
            self.chains.get_first_division())

        assert self.chains.check_if_chain_exist(chain) is False
        assert 'Підрозділ не в вашій організації' == result.get('error').get('message')





if __name__ == '__main__':
    pass
