import names
from requests import post

from ApiTests.BaseApiTestLogic import BaseApiTestLogic
from ApiTests.Helpers import dict_to_json, body_to_dict
from ApiTests.app_config import universal_password, operator_login, operator_password
from tools.data_generator import FakeHostEmailGenerator, generate_phone_number


class GenerateUserData:
    def __init__(self, custom=False, user_data=None):
        """On default generate random data, if custom=True, fill user_data dict"""
        if not custom:
            self.name = names.get_first_name()
            self.surname = names.get_last_name()
            self.email_address = self.name + self.surname + FakeHostEmailGenerator().fake_email_host()
            self.password = universal_password
            self.phone = generate_phone_number()
        else:
            self.name = user_data['FirstName']
            self.surname = user_data['LastName']
            self.email_address = user_data['EmailAddress']
            self.password = user_data['Password']
            self.phone = user_data['Phone']

    def get_attr(self):
        return vars(self)


class User(BaseApiTestLogic):
    def __init__(self, login, password=universal_password, data=None):
        self.headers = BaseApiTestLogic.set_headers(login, password)
        self.empty_body_request = BaseApiTestLogic.empty_body_request
        self.email_address = login
        self.data = data  # data from DB

    def get_current_user(self):
        request = post(url=self.base_url + 'api/services/etender/user/GetCurrentUser',
                       headers=self.headers,
                       data=self.empty_body_request)
        return body_to_dict(request.content)['result']

    @property
    def is_can_organization_create(self):
        # TODO: should it be in Organization?
        request = post(url=self.base_url + 'api/services/etender/organization/IsCanOrganizationCreate',
                       headers=self.headers,
                       data=self.empty_body_request)
        return body_to_dict(request.content)['result']


class Operator(User):
    def __init__(self, login=operator_login, password=operator_password):
        super().__init__(login, password)

    def activate_email_address(self, user_id):
        request = post(url=self.base_url + 'api/services/etender/user/ActivateUser',
                       headers=self.headers,
                       data=dict_to_json({'Id': int(user_id)}))
        return body_to_dict(request.content)


if __name__ == '__main__':
    pass
