import names

from ApiTests.app_config import universal_password
from tools.fake_email_generator import fake_email_host
from ApiTests import Helpers


class GenerateUserData:
    def __init__(self):
        self.name = names.get_first_name()
        self.surname = names.get_last_name()
        self.email_address = self.name + self.surname + fake_email_host()
        self.password = universal_password
        self.phone = Helpers.generate_phone()

    def get_attr(self):
        return vars(self)
