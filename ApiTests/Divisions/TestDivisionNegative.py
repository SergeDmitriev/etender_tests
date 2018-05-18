import pytest

from ApiTests.Divisions.TestDivision import Division, UpdateDivision


class DivisionNegative(Division):
    pass


@pytest.mark.usefixtures("create_division")
class TestUpdateDivisionNegative(UpdateDivision):

    def test_update_division(self):
        print('a')

    def test_update_division_2(self):
        print('b')

    # def test_update_not_existing_division(self):
    #     # TODO: remove hardcoded and make parametrize
    #     new_division_title = 'Division not exists'
    #     division = {'id': 0, 'title': 'Not existing Department'}
    #     result = self.update_division(division, new_division_title)
    #     assert result.get('error').get('message') == 'Division is not in your organization'
    #
    # def test_update_not_mine_division(self):
    #     # TODO: remove hardcoded and make parametrize
    #     new_division_title = 'Division not exists'
    #     division = {'id': 1, 'title': 'Department not in my organization'}
    #     result = self.update_division(division, new_division_title)
    #     assert result.get('error').get('message') == 'Division is not in your organization'

if __name__ == "__main__":
    pass
