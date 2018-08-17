from ApiTests.Application.Models.UserModel import Operator
from ApiTests.Application.Registration import RegistrationHelper
from ApiTests.BaseApiTestLogic import BaseApiTestLogic


class TestRegisterUser(BaseApiTestLogic):
    user = RegistrationHelper()

    def test_first_step(self):

        if self.user.check_if_user_exist(self.user.user_data['EmailAddress']) is False:
            result = self.user.register_user()
            assert True is result['success']
            assert True is self.user.check_if_user_exist(self.user.user_data['EmailAddress'])
            print(self.get_obj_attr(self.user))

        elif self.user.check_if_user_exist(self.user.user_data['EmailAddress']) is True:
            print('User already exists in DB!')

    def test_confirm_email_address_via_link(self):
        user_info = self.user.get_info_about_user(self.user.user_data['EmailAddress'])
        confirmation = self.user.confirm_email(user_info['EmailConfirmationCode'], user_info['id'])
        user_info_after = self.user.get_info_about_user(self.user.user_data['EmailAddress'])

        assert 0 == user_info['IsEmailConfirmed']
        assert True is self.check_success_status(confirmation)
        assert 1 == user_info_after['IsEmailConfirmed']
        assert None is user_info_after['EmailConfirmationCode']



class TestOperatorConfirmation(BaseApiTestLogic):
    # TODO: refactor, too much redundant code, unproductive code usage
    def test_confirm_email_address_via_operator(self, login_as_operator):

        # Generate user data and check if he created successfully
        user_to_register = RegistrationHelper()
        if user_to_register.check_if_user_exist(user_to_register.user_data['EmailAddress']) is False:
            result = user_to_register.register_user()
            assert True is result['success']
            assert True is user_to_register.check_if_user_exist(user_to_register.user_data['EmailAddress'])

        elif user_to_register.check_if_user_exist(user_to_register.user_data['EmailAddress']) is True:
            print('User already exists in DB!')
        user_id = user_to_register.get_info_about_user(user_to_register.user_data['EmailAddress'])['id']
        # Login as operator and activate user email
        confirmation_result = Operator().activate_email_address(user_id)

        user_info_after = user_to_register.get_info_about_user(user_to_register.user_data['EmailAddress'])
        assert True is confirmation_result['success']
        assert 1 == user_info_after['IsEmailConfirmed']
        assert None is user_info_after['EmailConfirmationCode']
