import json

from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Divisions.Division import Division


def test_update_division_negative(create_division_obj, division_update_parametrized):
    # using fixtures: create_division_obj AND division_update_parametrized
    result = create_division_obj.update_division(division_update_parametrized.get('division'),
                                                 division_update_parametrized.get('new_division_title'))
    assert 'Підрозділ не в вашій організації' == result.get('error').get('message')


class TestDeleteDivisionNegative(BaseApiTestLogic):

    division = Division()

    def test_delete_not_existing_division(self):
        # TODO: remove hardcoded and make parametrize, DEL NOT MINE DIVISION
        old_existing_division = {'id': 38, 'title': 'QA Department'}
        request = self.division.delete_division(old_existing_division)
        assert json.loads(request).get('error').get('message') == 'Підрозділ не в вашій організації'
        self.division.assert_division_not_exist(old_existing_division)


if __name__ == "__main__":
    pass
