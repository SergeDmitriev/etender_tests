# region Division
from ApiTests.app_config import division_admin_login, universal_password, division_manager_four_login, \
    division_manager_one_login, division_head_of_dep_one_login

update_division_test_data = [
    {'test_name': 'Not existing Department',
     'new_division_title': 'Division not exists', 'division': {'id': 0, 'title': 'Not existing Department'}},
    {'test_name': 'Department not in my organization',
     'new_division_title': 'Division not mine', 'division': {'id': 5, 'title': 'Department not in my organization'}}
                            ]

# add_user_to_division_data = [
#     {'test_name': 'Positive. User, division belongs to organization',
#      'userId': DivisionExts()._division_head_of_dep_one.get('UserId'),
#      'divisionId': DivisionExts().get_exact_division()},
#
#     {'test_name': 'Negative. Not existing division',
#      'userId': DivisionExts()._division_head_of_dep_one.get('UserId'),
#      'divisionId': {'id': 0, 'title': 'Not existing Department'}}
#                             ]

# delete_user_to_division_data = [
#     {'userId': {'UserId': '0', 'Email': 'nonexistentUser@division.com'},
#      'division': {'id': 35, 'title': 'test'}
#     }
# ]
# endregion Division

# region GetTenders
get_tenders_parameters = [
    {'test_name': 'Get Test Competitive Procedures',
     'tab': 'competitive', 'mode': None, 'show_real_checkbox': False},
    {'test_name': 'Get Test Noncompetitive Procedures',
     'tab': 'noncompetitive', 'mode': None, 'show_real_checkbox': False},
    {'test_name': 'Get Real Competitive Procedures from test mode',
     'tab': 'competitive', 'mode': None, 'show_real_checkbox': True},
    {'test_name': 'Get Real Noncompetitive Procedures from test mode',
     'tab': 'noncompetitive', 'mode': None, 'show_real_checkbox': True}
    # ,{'test_name': 'Get Real Competitive Procedures',
    #  'tab': 'competitive', 'mode': True, 'show_real_checkbox': False},
    # {'test_name': 'Get Real Noncompetitive Procedures',
    #  'tab': 'noncompetitive', 'mode': True, 'show_real_checkbox': False}
                         ]
# endregion GetTenders


# region GetTendersWithResponsibles
"""get_tenders_with_responsiles_parameters - tuple, for """
get_tenders_with_responsibles_users = [
    (division_admin_login, universal_password, ),
    (division_head_of_dep_one_login, universal_password, ),
    (division_manager_one_login, universal_password, ),
    (division_manager_four_login, universal_password, )
]
# endregion GetTendersWithResponsibles


if __name__ == '__main__':
    pass
