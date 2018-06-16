from ApiTests.Divisions.Division import DivisionUserChain

update_division_test_data = [
    {'new_division_title': 'Division not exists', 'division':{'id': 0, 'title': 'Not existing Department'}},
    {'new_division_title': 'Division not mine', 'division':{'id': 1, 'title': 'Department not in my organization'}}
                            ]

add_user_to_division_data = [
    {'test_name': 'Positive. User, division belongs to organization',
     'userId': DivisionUserChain()._division_head_of_dep_one.get('UserId'),
     'divisionId': DivisionUserChain().get_first_division()},

    {'test_name': 'Negative. Not existing division',
     'userId': DivisionUserChain()._division_head_of_dep_one.get('UserId'),
     'divisionId': {'id': 0, 'title': 'Not existing Department'}}
                            ]

delete_user_to_division_data = [
    {'userId': {'UserId': '0', 'Email': 'nonexistentUser@division.com'},
     'division': {'id': 35, 'title': 'test'}
    },

    {'userId': ''},
]


if __name__ == '__main__':
    pass
