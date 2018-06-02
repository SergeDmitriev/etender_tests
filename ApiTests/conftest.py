import pytest
from ApiTests.Divisions.Division import Division
from ApiTests.etender_data_api import update_division_test_data, \
    add_user_to_division_data


@pytest.fixture
def create_division_obj():
    """Create empty object"""
    division = Division()
    return division


@pytest.fixture(params=update_division_test_data, ids=['Not existing Department', 'Department not in my organization'])
def division_update_parametrized(request):
    return request.param


@pytest.fixture(params=add_user_to_division_data, ids=[item.get('test_name') for item in add_user_to_division_data])
def add_user_to_division_parametrized(request):
    yield request.param
