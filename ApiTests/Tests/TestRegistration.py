from ApiTests.Application.Registration import RegisterUser
from ApiTests.BaseApiTestLogic import BaseApiTestLogic


class TestRegisterUser(BaseApiTestLogic):
    def test_first_step(self):
        user = RegisterUser()

        if user.check_if_user_exist(user.user_data['EmailAddress']) is False:
            result = user.register_user()
            assert True is result['success']
            assert True is user.check_if_user_exist(user.user_data['EmailAddress'])
            print(self.get_ob_attr(user))

        elif user.check_if_user_exist(user.user_data['EmailAddress']) is True:
            print('User already exists in DB!')

