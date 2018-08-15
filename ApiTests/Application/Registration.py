from requests import post

from ApiTests.Application.Models.User import GenerateUserData
from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Helpers import dict_to_json, body_to_dict
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

    def register_user(self):
        """fill info about contactpoint"""
        request = post(url=self.base_url + 'Account/Register',
                       headers=self.headers,
                       data=dict_to_json(self.user_data))
        return body_to_dict(request.content)


if __name__ == '__main__':
    user = RegisterUser()
    print(user.check_if_user_exist('lrn40387@sqoai.com'))
