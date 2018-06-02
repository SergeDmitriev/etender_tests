from ApiTests.Divisions.Division import DivisionUsersInOrganization

update_division_test_data = [
    {'new_division_title': 'Division not exists', 'division':{'id': 0, 'title': 'Not existing Department'}},
    {'new_division_title': 'Division not mine', 'division':{'id': 1, 'title': 'Department not in my organization'}}
                            ]



add_user_to_division_data = [
    {'test_name': 'Positive. User, division belongs to organization',
     'userId': DivisionUsersInOrganization()._division_head_of_dep_one.get('UserId'),
     'divisionId': DivisionUsersInOrganization().get_first_division()},

    {'test_name': 'Negative. Not existing division',
     'userId': DivisionUsersInOrganization()._division_head_of_dep_one.get('UserId'),
     'divisionId': {'id': 0, 'title': 'Not existing Department'}}


                            ]


if __name__ == '__main__':
    pass

