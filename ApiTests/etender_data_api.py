base_prozorro_url = 'http://52.138.214.244/'


class DivisionUsersOrganization(object):
    _division_admin = {'UserId': '1247', 'Email': 'divisionAdmin@division.com'}
    _division_head_of_dep_one = {'UserId': '1248', 'Email': 'divisionHeadOfDepOne@division.com'}
    _division_head_of_dep_two = {'UserId': '1249', 'Email': 'divisionHeadOfDepTwo@division.com'}
    _division_head_of_deps_one = {'UserId': '1250', 'Email': 'divisionHeadOfDepsOne@division.com'}
    _division_head_of_deps_two = {'UserId': '1251', 'Email': 'divisionHeadOfDepsTwo@division.com'}
    _division_manager_one = {'UserId': '1252', 'Email': 'divisionManagerOne@division.com'}
    _division_manager_two = {'UserId': '1253', 'Email': 'divisionManagerTwo@division.com'}
    _division_manager_three = {'UserId': '1254', 'Email': 'divisionManagerThree@division.com'}
    _division_manager_four = {'UserId': '1255', 'Email': 'divisionManagerFour@division.com'}
    _unassigned_user_to_division = {'UserId': '1266', 'Email': 'UnassignedUserToDivision@division.com'}





if __name__ == '__main__':
    obj = DivisionUsersOrganization()
    print(obj._division_admin)

