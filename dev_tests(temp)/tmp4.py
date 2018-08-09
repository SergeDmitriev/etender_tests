from ApiTests.app_config import division_admin_login
from ApiTests.etender_data_api import division_admin, division_head_of_dep_one

data_for_assign_user = [
    {'test_name': 'Admin assign tender to Admin', 'who_assign': division_admin_login,
     'assign_to': division_admin, 'can_assign': True},
    {'test_name': 'Admin assign tender to HeadOfDepOne', 'who_assign': division_admin_login,
     'assign_to': division_head_of_dep_one, 'can_assign': True}]


def f(lst):
    for i in lst:
        i['test_name'] = i['test_name'].replace('assign tender to', 'unassigned tender from')
    return lst


if __name__ == '__main__':
    print(f(data_for_assign_user))