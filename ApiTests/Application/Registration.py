import pytest
from requests import post

from ApiTests.Application.Models.UserModel import GenerateUserData
from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Helpers import dict_to_json, body_to_dict, convert_to_dict
from db_layer.DB_table_fields import AbpUsersTableFields
from db_layer.db_application import send_query
from db_layer.sql_queries import select_where_email_equal


class RegisterUser(BaseApiTestLogic):
    """On default - generate random data for registration"""

    def __init__(self, user_obj=GenerateUserData()):
        self.headers = BaseApiTestLogic.set_headers('', '', cookie=False)
        self.user_data = {"EmailAddress": user_obj.email_address,
                          "Password": user_obj.password,
                          "FirstName": user_obj.name,
                          "LastName": user_obj.surname,
                          "Phone": user_obj.phone}

    def register_user(self):
        """fill info about contactpoint"""
        request = post(url=self.base_url + 'Account/Register',
                       headers=self.headers,
                       data=dict_to_json(self.user_data))
        return body_to_dict(request.content)

    def confirm_email(self, code, user_id):
        request = post(url=self.base_url + 'Account/ConfirmEmail',
                       headers=self.headers,
                       data=dict_to_json({'Code': code,
                                          'UserId': int(user_id)}))
        return body_to_dict(request.content)


class RegistrationHelper(RegisterUser):

    def __init__(self, user_obj=GenerateUserData()):
        super().__init__(user_obj)

    def check_if_user_exist(self, user_email):
        """check by email, field is unique in DB"""
        result = send_query(select_where_email_equal(user_email))
        if not result:
            return False
        elif user_email in result[0] and len(result) == 1:
            return True
        else:
            print('Something goes wrong! Investigate!')
            raise AssertionError

    def get_info_about_user(self, user_email):
        try:
            user = send_query(select_where_email_equal(user_email))[0]
            return convert_to_dict(AbpUsersTableFields, user)
        except IndexError:
            return None


if __name__ == '__main__':
    # my = {"EmailAddress": 'eqp79667@auoie.com',
    #      "Password": 'Qq123456',
    #      "FirstName": 'name',
    #      "LastName": 'surname',
    #      "Phone": '111111111111'}
    # user = GenerateUserData(custom=True, user_data=my)
    # print(vars(user))
    pass
