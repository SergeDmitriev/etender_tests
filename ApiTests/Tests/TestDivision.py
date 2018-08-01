import json
import pytest

from ApiTests.Application.Tender import ToDoTenders
from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Application.Division import Division, DivisionExts
from ApiTests.Helpers import update_keys
from ApiTests.app_config import division_admin_login, universal_password


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


def test_update_division_negative(create_division_obj, division_update_parametrized):
    # using fixtures: create_division_obj AND division_update_parametrized
    result = create_division_obj.update_division(division_update_parametrized.get('division'),
                                                 division_update_parametrized.get('new_division_title'))
    assert False is create_division_obj.check_success_status(result)
    assert 'Підрозділ не в вашій організації' == result.get('error').get('message')


def test_delete_not_existing_division(create_division_obj):
    old_existing_division = {'id': 0, 'title': 'QA Department'}
    request = create_division_obj.delete_division(old_existing_division)
    assert False is create_division_obj.check_success_status(request)
    assert json.loads(request).get('error').get('message') == 'Підрозділ не в вашій організації'
    create_division_obj.assert_division_not_exist(old_existing_division)


class TestAddHeadToDivision(BaseApiTestLogic):
    # Add head to division
    # TODO: много одинакового кода
    chains = DivisionExts()

    user_div = chains.group_user_and_division_into_chain(
        user=chains._division_head_of_dep_one,
        division=chains.get_exact_division())

    def test_add_user_to_division_as_head(self):
        """Positive case, if chain already exists - drop it first
        Parameter isHead not sent while adding to division"""
        user = self.chains.group_user_and_division_into_chain(
            user=self.chains._division_head_of_dep_one,
            division=self.chains.get_exact_division())

        if self.chains.check_if_chain_exist(user):
            # Delete user_division chain from DB
            self.chains.delete_user_from_division(
                self.chains._division_head_of_dep_one,
                self.chains.get_exact_division())
            assert self.chains.check_if_chain_exist(user) is False

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=self.chains._division_head_of_dep_one,
            division=self.chains.get_exact_division(),
            isHead=1)
        assert self.chains.check_if_chain_exist(user) is True
        assert self.chains.check_isHead(self.chains.user_division_chain) is True

    @pytest.mark.xfail
    def test_add_nonexistent_user_to_division_as_head(self):
        all_chains = self.chains.get_all_user_division_chains()
        user_to_add = {'userid': '0', 'Email': 'nonexistentUser@division.com', 'isHead': 1}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=self.chains.get_exact_division(),
            isHead=1)

        assert user_to_add not in all_chains
        assert self.chains.user_division_chain.get('error').get('message') \
               == 'You in different organization with user try to add'
        raise AssertionError  # response not correct

    @pytest.mark.xfail
    def test_add_user_to_nonexistent_division_as_head(self):
        all_chains = self.chains.get_all_user_division_chains()
        user_to_add = self.chains._unassigned_user_to_division
        nonexistent_division = {'id': 0, 'title': 'Nonexistent division', 'isHead': 1}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=nonexistent_division,
            isHead=1)

        assert self.chains.group_user_and_division_into_chain(user=user_to_add,
                                                              division=nonexistent_division) not in all_chains
        assert 'Підрозділ не в вашій організації' == self.chains.user_division_chain.get('error').get('message')
        raise AssertionError  # response not correct

    @pytest.mark.xfail
    def test_add_user_if_chain_exists_as_head(self):
        if not self.chains.check_if_chain_exist(self.user_div):
            self.chains.user_division_chain = self.chains.add_user_to_division(
                user=self.chains._division_head_of_dep_one,
                division=self.chains.get_exact_division(),
                isHead=1)
            assert self.chains.check_if_chain_exist(self.user_div)
            assert True is self.chains.check_isHead(self.chains.user_division_chain)

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=self.chains._division_head_of_dep_one,
            division=self.chains.get_exact_division(),
            isHead=1)

        assert 'User in this division already exist' == \
               self.chains.user_division_chain.get('error').get('message')

        self.chains.delete_user_from_division(self.chains._division_head_of_dep_one, self.chains.get_exact_division())
        assert self.chains.check_if_chain_exist(self.user_div) is False
        raise AssertionError  # response not correct

    def test_add_user_to_foreign_division_as_head(self):
        all_chains = self.chains.get_all_user_division_chains()
        # TODO: all_chains can be None! create preconditions
        user_to_add = self.chains._unassigned_user_to_division
        foreign_division = {'id': 5, 'Підрозділ тестування': 'test', 'isHead': 1}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=foreign_division,
            isHead=1)

        assert self.chains.group_user_and_division_into_chain(user=user_to_add,
                                                              division=foreign_division) not in all_chains
        assert 'Підрозділ не в вашій організації' == self.chains.user_division_chain.get('error').get('message')

    @pytest.mark.xfail
    def test_add_foreign_user_to_division_as_head(self):
        all_chains = self.chains.get_all_user_division_chains()
        # TODO remove hardcore
        user_to_add = {'userid': '1', 'Email': 'not_my_user@test.com', 'isHead': 1}
        division = self.chains.get_exact_division()

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=division,
            isHead=1)

        assert 'You in different organization with user try to add' == \
               self.chains.user_division_chain.get('error').get('message')
        assert user_to_add not in all_chains
        raise AssertionError  # response not correct


class TestAddManagerToDivision(BaseApiTestLogic):
    # Add manager to division
    # TODO: много одинакового кода
    chains = DivisionExts()

    user_div = chains.group_user_and_division_into_chain(
        user=chains._division_manager_one,
        division=chains.get_exact_division())

    def test_add_user_to_division_as_manager(self):
        """Positive case, if chain already exists - drop it first
        isHead = null"""
        user = self.chains.group_user_and_division_into_chain(
            user=self.chains._division_manager_one,
            division=self.chains.get_exact_division())

        if self.chains.check_if_chain_exist(user):
            # Delete user_division chain from DB
            self.chains.delete_user_from_division(
                self.chains._division_manager_one,
                self.chains.get_exact_division())
            assert self.chains.check_if_chain_exist(user) is False

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=self.chains._division_manager_one,
            division=self.chains.get_exact_division())
        assert self.chains.check_if_chain_exist(user)
        assert False == self.chains.check_isHead(self.chains.user_division_chain)

    @pytest.mark.xfail
    def test_add_nonexistent_user_to_division_as_manager(self):
        all_chains = self.chains.get_all_user_division_chains()
        user_to_add = {'userid': '0', 'Email': 'nonexistentUser@division.com'}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=self.chains.get_exact_division())

        assert user_to_add not in all_chains and \
               self.chains.user_division_chain.get('error').get('message') \
               == 'You in different organization with user try to add'
        raise AssertionError  # response not correct

    @pytest.mark.xfail
    def test_add_user_to_nonexistent_division_as_manager(self):
        all_chains = self.chains.get_all_user_division_chains()
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
        raise AssertionError  # response not correct

    @pytest.mark.xfail
    def test_add_user_if_chain_exists_as_manager(self):
        if not self.chains.check_if_chain_exist(self.user_div):
            self.chains.user_division_chain = self.chains.add_user_to_division(
                user=self.chains._division_manager_one,
                division=self.chains.get_exact_division())
            assert self.chains.check_if_chain_exist(self.user_div)

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=self.chains._division_manager_one,
            division=self.chains.get_exact_division())

        assert 'User in this division already exist' == \
               self.chains.user_division_chain.get('error').get('message')
        raise AssertionError  # incorrect response

    def test_add_user_to_foreign_division_as_manager(self):
        all_chains = self.chains.get_all_user_division_chains()
        # TODO: all_chains can be None! create preconditions
        user_to_add = self.chains._division_manager_one
        foreign_division = {'id': 5, 'title': 'Підрозділ тестування'}

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=foreign_division)

        assert self.chains.group_user_and_division_into_chain(
            user=user_to_add, division=foreign_division) \
               not in all_chains and \
               'Підрозділ не в вашій організації' == self.chains.user_division_chain.get('error').get('message')

    @pytest.mark.xfail
    def test_add_foreign_user_to_division_as_manager(self):
        all_chains = self.chains.get_all_user_division_chains()
        # TODO remove hardcore
        user_to_add = {'userid': '1', 'Email': 'not_my_user@test.com'}
        division = self.chains.get_exact_division()

        self.chains.user_division_chain = self.chains.add_user_to_division(
            user=user_to_add,
            division=division)

        assert 'You in different organization with user try to add' == \
               self.chains.user_division_chain.get('error').get('message')
        assert user_to_add not in all_chains
        raise AssertionError  # incorrect response message


class TestDeleteFromDivision(BaseApiTestLogic):
    # TODO: add preconditions, maybe parametrize
    chains = DivisionExts()

    # user - head of division
    def test_delete_user_from_division(self):
        user_div = self.chains.group_user_and_division_into_chain(
            user=self.chains._division_head_of_dep_one,
            division=self.chains.get_exact_division())
        add_user_back = True

        if not self.chains.check_if_chain_exist(user_div):
            # Add user:
            add_user_back = False
            self.chains.user_division_chain = self.chains.add_user_to_division(
                user=self.chains._division_head_of_dep_one,
                division=self.chains.get_exact_division())
            assert self.chains.check_if_chain_exist(user_div)

        self.chains.delete_user_from_division(
            self.chains._division_head_of_dep_one,
            self.chains.get_exact_division())
        assert self.chains.check_if_chain_exist(user_div) is False

        # finally: add user back (tearDown?)
        if add_user_back:
            self.chains.user_division_chain = self.chains.add_user_to_division(
                user=self.chains._division_head_of_dep_one,
                division=self.chains.get_exact_division(), isHead=True)

    def test_delete_user_from_nonexistent_division(self):
        nonexistent_division = {'id': 0, 'title': 'Nonexistent division'}

        chain = self.chains.group_user_and_division_into_chain(
            user=self.chains._division_head_of_dep_one,
            division=nonexistent_division)

        result = self.chains.delete_user_from_division(
            self.chains._division_head_of_dep_one,
            nonexistent_division)

        assert self.chains.check_if_chain_exist(chain) is False
        assert 'Підрозділ не в вашій організації' == result.get('error').get('message')

    def test_delete_nonexistent_user_from_division(self):
        # TODO: test fails now
        user_to_delete = {'userid': '0', 'Email': 'nonexistentUser@division.com'}

        chain = self.chains.group_user_and_division_into_chain(
            user=user_to_delete,
            division=self.chains.get_exact_division())

        result = self.chains.delete_user_from_division(
            user_to_delete,
            self.chains.get_exact_division())

        assert self.chains.check_if_chain_exist(chain) is False
        assert 'You in different organization with user try to add' == result.get('error').get('message')

    def test_delete_nonexistent_chain(self):
        user_to_delete = {'userid': '0', 'Email': 'nonexistentUser@division.com'}
        nonexistent_division = {'id': 0, 'title': 'Nonexistent division'}

        chain = self.chains.group_user_and_division_into_chain(
            user=user_to_delete,
            division=nonexistent_division)

        result = self.chains.delete_user_from_division(
            user_to_delete,
            nonexistent_division)

        assert self.chains.check_if_chain_exist(chain) is False
        assert 'Підрозділ не в вашій організації' == result.get('error').get('message')

    def test_delete_user_from_foreign_division(self):
        user_to_delete = {'userid': '0', 'Email': 'nonexistentUser@division.com'}
        foreign_division = {'id': 5, 'title': 'Підрозділ тестування'}

        chain = self.chains.group_user_and_division_into_chain(
            user=user_to_delete,
            division=foreign_division)

        result = self.chains.delete_user_from_division(
            user_to_delete,
            foreign_division)

        assert self.chains.check_if_chain_exist(chain) is False
        assert 'Підрозділ не в вашій організації' == result.get('error').get('message')

    def test_delete_foreign_user_from_division(self):
        user_to_delete = {'userid': '235', 'Email': 'turkobubro@meta.ua'}

        chain = self.chains.group_user_and_division_into_chain(
            user=user_to_delete,
            division=self.chains.get_exact_division())

        result = self.chains.delete_user_from_division(
            user_to_delete,
            self.chains.get_exact_division())

        assert self.chains.check_if_chain_exist(chain) == False
        assert 'You in different organization with user try to add' == result.get('error').get('message')


class TestAddUserToSeveralDivisions(BaseApiTestLogic):
    chains = DivisionExts()

    user = chains._unassigned_user_to_division

    def test_add_user_to_divisions_as_head(self):
        # user = self.chains._unassigned_user_to_division
        chains_as_head = self.chains.get_all_user_division_chains(show_isHead=True)
        chains_to_delete_as_head = self.chains.find_user_in_divisions(self.user, chains_as_head)

        if chains_to_delete_as_head:
            self.chains.delete_user_from_all_divisions(self.user, chains_to_delete_as_head)

        first = self.chains.add_user_to_division(user=self.user,
                                                 division=self.chains.get_exact_division(),
                                                 isHead=1).get('result')

        second = self.chains.add_user_to_division(user=self.user,
                                                  division=self.chains.get_exact_division(1),
                                                  isHead=1).get('result')

        first['userid'] = first.pop('userId')
        first['divisionid'] = first.pop('divisionId')
        first['isHead'] = first.pop('isHead')

        second['userid'] = second.pop('userId')
        second['divisionid'] = second.pop('divisionId')
        second['isHead'] = second.pop('isHead')

        new_chains_list = self.chains.get_all_user_division_chains(show_isHead=True)
        assert first in new_chains_list
        assert second in new_chains_list
        self.chains.delete_user_from_all_divisions(self.user,
                                                   self.chains.find_user_in_divisions(self.user, new_chains_list))

    def test_add_user_to_divisions_as_manager(self):

        chains_as_manager = self.chains.get_all_user_division_chains(show_isHead=True)
        chains_to_delete_as_manager = self.chains.find_user_in_divisions(self.user, chains_as_manager)

        if chains_to_delete_as_manager:
            self.chains.delete_user_from_all_divisions(self.user, chains_to_delete_as_manager)

        first = self.chains.add_user_to_division(user=self.user,
                                                 division=self.chains.get_exact_division(),
                                                 isHead=0).get('result')

        second = self.chains.add_user_to_division(user=self.user,
                                                  division=self.chains.get_exact_division(1), isHead=0).get('result')
        # update_keys(first, 'userid', 'userId')
        # update_keys(first, 'divisionid', 'divisionId')
        # update_keys(first, 'isHead', 'isHead')
        first['userid'] = first.pop('userId')
        first['divisionid'] = first.pop('divisionId')
        first['isHead'] = first.pop('isHead')

        second['userid'] = second.pop('userId')
        second['divisionid'] = second.pop('divisionId')
        second['isHead'] = second.pop('isHead')

        new_chains_list = self.chains.get_all_user_division_chains(show_isHead=True)
        assert first in new_chains_list
        assert second in new_chains_list
        self.chains.delete_user_from_all_divisions(self.user,
                                                   self.chains.find_user_in_divisions(self.user, new_chains_list))

    # def test_add_user_as_manager_if_he_is_head(self):
    #     user = self.chains._unassigned_user_to_division
    #
    #
    #     if self.chains_to_delete_as_head and self.chains_to_delete_as_manager:
    #         self.chains.delete_user_from_all_divisions(user, self.chains_to_delete_as_manager)
    #         self.chains.delete_user_from_all_divisions(user, self.chains_to_delete_as_head)

    # def test_add_user_as_head_if_he_is_manager(self):
    #     pass


class TestUpdateUserRoleInDivision(BaseApiTestLogic):
    chain = DivisionExts()
    user = chain._unassigned_user_to_division

    def test_update_head_role_to_manager(self):
        # TODO: deleting in cycle, prints to console lots odd info
        self.chain.delete_user_from_all_divisions(self.user,
                                                  self.chain.get_all_user_division_chains(show_isHead=True))
        adding_chain = self.chain.add_user_to_division(user=self.user,
                                                       division=self.chain.get_exact_division(),
                                                       isHead=True).get('result')
        update_keys(adding_chain, 'divisionId', 'divisionid')
        update_keys(adding_chain, 'userId', 'userid')
        assert adding_chain in self.chain.get_all_user_division_chains(True)

        updated_chain = self.chain.update_user_role(self.user, self.chain.get_exact_division(), False).get('result')
        assert False is updated_chain.get('isHead')

        update_keys(updated_chain, 'divisionId', 'id')
        self.chain.delete_user_from_division(self.user, updated_chain)

    def test_update_manager_role_to_head(self):
        # TODO: deleting in cycle, prints to console lots odd info
        self.chain.delete_user_from_all_divisions(self.user,
                                                  self.chain.get_all_user_division_chains(show_isHead=True))
        adding_chain = self.chain.add_user_to_division(user=self.user,
                                                       division=self.chain.get_exact_division()).get('result')
        update_keys(adding_chain, 'divisionId', 'divisionid')
        update_keys(adding_chain, 'userId', 'userid')

        assert adding_chain in self.chain.get_all_user_division_chains(True)

        updated_chain = self.chain.update_user_role(self.user, self.chain.get_exact_division(), True).get('result')
        assert True is updated_chain.get('isHead')

        update_keys(updated_chain, 'divisionId', 'id')
        self.chain.delete_user_from_division(self.user, updated_chain)


class TestGetToDoTenders(BaseApiTestLogic):
    # TODO: add assertion with db
    all_assigned = ToDoTenders(division_admin_login, universal_password)

    @pytest.fixture(autouse=True)
    def user(self, get_tenders_with_responsibles_obj):
        yield get_tenders_with_responsibles_obj

    def test_get_tenders_in_work(self, user):
        print('В РОБОТІ: ', user.count_all_records(user.get_tenders_with_responsibles('in_work')))

    def test_get_tenders_new(self, user):
        all_tenders_count = user.count_all_records(user.get_tenders_with_responsibles('new_tenders'))
        all_in_work = self.all_assigned.count_all_records(self.all_assigned.get_tenders_with_responsibles('in_work'))
        print(all_tenders_count - all_in_work)

    def test_get_tenders_archive(self, user):
        print(user.count_all_records(user.get_tenders_with_responsibles('archive')))


class TestSetResponsibleUserTender(BaseApiTestLogic):
    # TODO: if first 100 tenders are assigned, errors could be

    def test_assign_tender_to_user(self, assignment_user_for_tender_parameters):
        """all_tender_id_responsibles_chains - all users and tenders, that has chain
        tender_id_list - top 100 tenders in new_tenders tab, including assigned"""

        tenders_from_admin = ToDoTenders(division_admin_login, universal_password)

        all_tender_id_responsibles_chains = tenders_from_admin.get_all_assigned_users_for_tenders(
            tenders_from_admin.get_tenders_with_responsibles('in_work'))
        tender_id_list = tenders_from_admin.get_top_100_tender_ids()
        unassigned_tender_id = tenders_from_admin.get_list_unassigned_tender(all_tender_id_responsibles_chains,
                                                                             tender_id_list)[0]
        print('Tender to assign: {0}'.format(unassigned_tender_id))
        print('Logged in as: {0}'.format(assignment_user_for_tender_parameters['who_assign']))
        print('Assign to user: {0}'.format(assignment_user_for_tender_parameters['assign_to']['userid']))

        div = DivisionExts(assignment_user_for_tender_parameters['who_assign'])
        assignment_result = div.set_responsible_user_tender(unassigned_tender_id,
                                                            assignment_user_for_tender_parameters['assign_to'][
                                                                'userid'], False)
        print(assignment_result)

        if assignment_user_for_tender_parameters['can_assign'] is True:
            assert True is assignment_result['success']
            assert assignment_result['result']['tenderNewId'] == unassigned_tender_id
            assert str(assignment_result['result']['userId']) == assignment_user_for_tender_parameters['assign_to'][
                'userid']
            assert True is tenders_from_admin.assure_tender_assigned_to_user(unassigned_tender_id,
                                                                             assignment_user_for_tender_parameters[
                                                                                 'assign_to']['Email'])
        elif assignment_user_for_tender_parameters['can_assign'] is False:
            assert False is assignment_result['success']
            assert assignment_result['error']['message'] == 'Ви не маєте прав зробити цього користувача відповідальним'
            assert None is tenders_from_admin.assure_tender_assigned_to_user(unassigned_tender_id,
                                                                             assignment_user_for_tender_parameters[
                                                                                 'assign_to']['Email'])


if __name__ == '__main__':
    pass
