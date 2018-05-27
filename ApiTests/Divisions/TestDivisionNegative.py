import json

import pytest

from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Divisions.Division import Division

@pytest.fixture
def division_negative():
    division = Division()
    yield division
    print('finalize')



def test_update_division(division_negative):
    # TODO: remove hardcoded and make parametrize
    new_division_title = 'Division not exists'
    div = {'id': 0, 'title': 'Not existing Department'}
    result = division_negative.update_division(div, new_division_title)
    print('text', result.get('error').get('message'))
    assert 'Division is not in your organization' == result.get('error').get('message')

def test_update_not_mine_division(division_negative):
    # TODO: remove hardcoded and make parametrize
    new_division_title = 'Division not mine'
    division =  {'id': 1, 'title': 'Department not in my organization'}
    result = division_negative.division.update_division(division, new_division_title)
    assert 'Division is not in your organization' == result.get('error').get('message')


class TestDeleteDivisionNegative(BaseApiTestLogic):

    division = Division()

    def test_delete_not_existing_division(self):
        # TODO: remove hardcoded and make parametrize
        old_existing_division = {'id': 38, 'title': 'QA Department'}
        request = self.division.delete_division(old_existing_division)
        assert json.loads(request).get('error').get('message') == 'Division is not in your organization'
        self.division.assert_division_not_exist(old_existing_division)


if __name__ == "__main__":
    pass
