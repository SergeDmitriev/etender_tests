import pytest
from ApiTests.Application.Division import Division
from ApiTests.Application.GetTenders import ToDoTenders
from ApiTests.Helpers import set_ids_for_fixture
from ApiTests.etender_data_api import update_division_test_data, get_tenders_parameters, \
    get_tenders_with_responsibles_users, user_names, users_for_assignment_to_tender, data_for_assign_user, \
    data_for_unassign_user_from_tender


# region Division
@pytest.fixture
def create_division_obj():
    """Create empty object"""
    division = Division()
    return division


@pytest.fixture(params=update_division_test_data, ids=set_ids_for_fixture(update_division_test_data))
def division_update_parametrized(request):
    return request.param
# endregion Division


# region GetTenders
@pytest.fixture(params=get_tenders_parameters, ids=set_ids_for_fixture(get_tenders_parameters))
def get_tenders_tab_parametrized(request):
    return request.param
# endregion GetTenders


# region GetTendersWithResponsibles
@pytest.fixture(params=get_tenders_with_responsibles_users,
                ids=user_names)
def get_tenders_with_responsibles_obj(request):
    obj = ToDoTenders(*request.param)
    yield obj
    del obj
# endregion GetTendersResponsibles


@pytest.fixture(params=data_for_assign_user, ids=set_ids_for_fixture(data_for_assign_user))
def assignment_user_for_tender_parameters(request):
    yield {'who_assign': request.param['who_assign'],
           'assign_to': request.param['assign_to'],
           'can_assign': request.param['can_assign']}


@pytest.fixture(params=data_for_unassign_user_from_tender, ids=set_ids_for_fixture(data_for_unassign_user_from_tender))
def unassign_user_from_tender_parameters(request):
    yield {'who_assign': request.param['who_assign'],
           'assign_to': request.param['assign_to'],
           'can_assign': request.param['can_assign']}


if __name__ == '__main__':
    pass
