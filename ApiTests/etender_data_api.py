# region Division
from ApiTests.Helpers import change_test_name
from ApiTests.app_config import division_admin_login, universal_password, \
    division_manager_one_login, division_head_of_dep_one_login, division_manager_three_login, \
    division_head_of_dep_two_login

division_admin = {'userid': '1247', 'Email': 'divisionAdmin@division.com', 'isHead': 0}
division_head_of_dep_one = {'userid': '1248', 'Email': 'divisionHeadOfDepOne@division.com', 'isHead': 1}
division_head_of_dep_two = {'userid': '1249', 'Email': 'divisionHeadOfDepTwo@division.com', 'isHead': 1}
division_head_of_deps_one = {'userid': '1250', 'Email': 'divisionHeadOfDepsOne@division.com', 'isHead': 1}
division_head_of_deps_two = {'userid': '1251', 'Email': 'divisionHeadOfDepsTwo@division.com', 'isHead': 1}
division_manager_one = {'userid': '1252', 'Email': 'divisionManagerOne@division.com', 'isHead': 0}
division_manager_two = {'userid': '1253', 'Email': 'divisionManagerTwo@division.com', 'isHead': 0}
division_manager_three = {'userid': '1254', 'Email': 'divisionManagerThree@division.com', 'isHead': 0}
division_manager_four = {'userid': '1255', 'Email': 'divisionManagerFour@division.com', 'isHead': 0}
unassigned_user_to_division = {'userid': '1266', 'Email': 'UnassignedUserToDivision@division.com', 'isHead': 0}
user_from_foreign_organization = {'userid': '235', 'Email': 'turkobubro@meta.ua', 'isHead': 0}

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
"""get_tenders_with_responsiles_parameters - tuple, for login"""
get_tenders_with_responsibles_users = [
    (division_admin_login, universal_password,),
    (division_head_of_dep_one_login, universal_password,),
    (division_manager_one_login, universal_password,),
    (division_manager_three_login, universal_password,)
]

user_names = [division_admin_login,
              division_head_of_dep_one_login,
              division_manager_one_login,
              division_manager_three_login]

users_for_assignment_to_tender = [division_admin['userid'],
                                  division_head_of_dep_one['userid'],
                                  division_manager_one['userid'],
                                  division_manager_three['userid']]
# endregion GetTendersWithResponsibles


# region AssignUsersForTender
data_for_assign_user = [
    {'test_name': 'Admin assign tender to Admin', 'who_assign': division_admin_login,
     'assign_to': division_admin, 'can_assign': True},
    {'test_name': 'Admin assign tender to HeadOfDepOne', 'who_assign': division_admin_login,
     'assign_to': division_head_of_dep_one, 'can_assign': True},
    {'test_name': 'Admin assign tender to ManagerOne', 'who_assign': division_admin_login,
     'assign_to': division_manager_one, 'can_assign': True},
    {'test_name': 'Admin assign tender to ManagerThree', 'who_assign': division_admin_login,
     'assign_to': division_manager_three, 'can_assign': True},
    {'test_name': 'Admin assign tender to Unassigned user for division', 'who_assign': division_admin_login,
     'assign_to': unassigned_user_to_division, 'can_assign': True},
    {'test_name': 'Admin assign tender to foreign user', 'who_assign': division_admin_login,
     'assign_to': user_from_foreign_organization, 'can_assign': False},

    {'test_name': 'HeadOfDepOne assign tender to Admin', 'who_assign': division_head_of_dep_one_login,
     'assign_to': division_admin, 'can_assign': False},
    {'test_name': 'HeadOfDepOne assign tender to HeadOfDepOne', 'who_assign': division_head_of_dep_one_login,
     'assign_to': division_head_of_dep_one, 'can_assign': True},
    {'test_name': 'HeadOfDepOne assign tender to ManagerOne', 'who_assign': division_head_of_dep_one_login,
     'assign_to': division_manager_one, 'can_assign': True},
    {'test_name': 'HeadOfDepOne assign tender to ManagerThree', 'who_assign': division_head_of_dep_one_login,
     'assign_to': division_manager_three, 'can_assign': False},
    {'test_name': 'HeadOfDepOne assign tender to HeadOfDepTwo', 'who_assign': division_head_of_dep_two_login,
     'assign_to': division_head_of_dep_two, 'can_assign': True},
    {'test_name': 'HeadOfDepOne assign tender to Unassigned user for division',
     'who_assign': division_head_of_dep_two_login, 'assign_to': unassigned_user_to_division, 'can_assign': False},

    {'test_name': 'ManagerOne assign tender to Admin', 'who_assign': division_manager_one_login,
     'assign_to': division_admin, 'can_assign': False},
    {'test_name': 'ManagerOne assign tender to HeadOfDepOne', 'who_assign': division_manager_one_login,
     'assign_to': division_head_of_dep_one, 'can_assign': False},
    {'test_name': 'ManagerOne assign tender to ManagerOne', 'who_assign': division_manager_one_login,
     'assign_to': division_manager_one, 'can_assign': True},
    {'test_name': 'ManagerOne assign tender to ManagerThree', 'who_assign': division_manager_one_login,
     'assign_to': division_manager_three, 'can_assign': False},
    {'test_name': 'ManagerOne assign tender to Unassigned user for division', 'who_assign': division_manager_one_login,
     'assign_to': unassigned_user_to_division, 'can_assign': False},

    {'test_name': 'ManagerThree assign tender to Admin', 'who_assign': division_manager_three_login,
     'assign_to': division_admin, 'can_assign': False},
    {'test_name': 'ManagerThree assign tender to HeadOfDepOne', 'who_assign': division_manager_three_login,
     'assign_to': division_head_of_dep_one, 'can_assign': False},
    {'test_name': 'ManagerThree assign tender to ManagerOne', 'who_assign': division_manager_three_login,
     'assign_to': division_manager_one, 'can_assign': False},
    {'test_name': 'ManagerThree assign tender to ManagerThree', 'who_assign': division_manager_three_login,
     'assign_to': division_manager_three, 'can_assign': True}
]

data_for_unassign_user_from_tender = change_test_name(data_for_assign_user, 'assign tender to',
                                                      'unassigned tender from')
# endregion AssignUsersForTender


if __name__ == '__main__':
    pass
