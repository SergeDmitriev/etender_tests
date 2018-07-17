import pytest
from ApiTests.Application.Division import Division
from ApiTests.Application.Tender import ToDoTenders
from ApiTests.Helpers import set_ids_for_fixture
from ApiTests.app_config import division_admin_login, division_head_of_dep_one_login, division_manager_one_login, \
    division_manager_four_login
from ApiTests.etender_data_api import update_division_test_data, get_tenders_parameters, \
    get_tenders_with_responsibles_users


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
@pytest.fixture(params=get_tenders_with_responsibles_users, ids=[division_admin_login,
                                                                 division_head_of_dep_one_login,
                                                                 division_manager_one_login,
                                                                 division_manager_four_login])
def get_tenders_with_responsibles_obj(request):
    obj = ToDoTenders(*request.param)
    yield obj
    del obj

# endregion GetTendersResponsibles


if __name__ == '__main__':
    pass

