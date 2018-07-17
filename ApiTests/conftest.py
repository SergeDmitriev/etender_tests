import pytest

from ApiTests.Application.Division import Division
from ApiTests.etender_data_api import update_division_test_data


@pytest.fixture
def create_division_obj():
    """Create empty object"""
    division = Division()
    return division


@pytest.fixture(params=update_division_test_data, ids=['Not existing Department', 'Department not in my organization'])
def division_update_parametrized(request):
    return request.param
