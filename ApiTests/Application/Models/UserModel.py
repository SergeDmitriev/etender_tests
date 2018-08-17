import names
import pytest
from requests import post

from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Helpers import dict_to_json, body_to_dict
from ApiTests.app_config import universal_password, operator_login, operator_password
from tools.fake_email_generator import fake_email_host
from ApiTests import Helpers


class GenerateUserData:
    def __init__(self, custom=False, user_data=None):
        """On default generate random data, if custom=True, fill user_data dict"""
        if not custom:
            self.name = names.get_first_name()
            self.surname = names.get_last_name()
            self.email_address = self.name + self.surname + fake_email_host()
            self.password = universal_password
            self.phone = Helpers.generate_phone()
        else:
            self.name = user_data['FirstName']
            self.surname = user_data['LastName']
            self.email_address = user_data['EmailAddress']
            self.password = user_data['Password']
            self.phone = user_data['Phone']

    def get_attr(self):
        return vars(self)


class Operator(BaseApiTestLogic):

    def __init__(self, login=operator_login, password=operator_password):
        self.headers = BaseApiTestLogic.set_headers(login, password)

    @pytest.fixture(autouse=True)
    def operator(self):
        yield BaseApiTestLogic().set_headers(operator_login, operator_password)

    def activate_email_address(self, user_id):
        request = post(url=self.base_url + 'api/services/etender/user/ActivateUser',
                       headers=self.headers,
                       data=dict_to_json({'Id': int(user_id)}))
        return body_to_dict(request.content)
