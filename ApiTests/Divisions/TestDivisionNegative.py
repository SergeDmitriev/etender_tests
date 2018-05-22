import json
from ApiTests.Divisions.TestDivision import UpdateDivision, DeleteDivision


# @pytest.mark.usefixtures('precondition_create_division')
class TestUpdateDivisionNegative(UpdateDivision):

    def test_update_division(self):
        # TODO: remove hardcoded and make parametrize
        new_division_title = 'Division not exists'
        division = {'id': 0, 'title': 'Not existing Department'}
        result = self.update_division(division, new_division_title)
        assert result.get('error').get('message') == 'Division is not in your organization'

    def test_update_not_mine_division(self):
        # TODO: remove hardcoded and make parametrize
        new_division_title = 'Division not exists'
        division = {'id': 1, 'title': 'Department not in my organization'}
        result = self.update_division(division, new_division_title)
        assert result.get('error').get('message') == 'Division is not in your organization'


class TestDeleteDivisionNegative(DeleteDivision):

    def test_delete_not_existing_division(self):
        # TODO: remove hardcoded and make parametrize
        old_existing_division = {'id': 38, 'title': 'QA Department'}
        request = self.delete_division(old_existing_division)
        assert json.loads(request).get('error').get('message') == 'Division is not in your organization'
        self.assert_division_not_exist(old_existing_division)


if __name__ == "__main__":
    pass
