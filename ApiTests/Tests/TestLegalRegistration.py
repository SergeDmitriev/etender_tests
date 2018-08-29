from ApiTests.Application.Models.OrganizationModel import Organization
from ApiTests.Application.Models.UserModel import User
from ApiTests.Application.Registration import RegistrationHelper
from ApiTests.BaseApiTestLogic import BaseApiTestLogic


class TestLegalEntityOrganizationAsCustomer(BaseApiTestLogic):
    user = RegistrationHelper()

    created_organization = None

    def test_first_step_registration(self):
        if self.user.check_if_user_exist(self.user.user_data['EmailAddress']) is False:
            result = self.user.register_user()
            assert True is result['success']
            assert True is self.user.check_if_user_exist(self.user.user_data['EmailAddress'])

            self.user.end_to_end_registration_user_data = \
                self.user.get_info_about_user(self.user.user_data['EmailAddress'])

        elif self.user.check_if_user_exist(self.user.user_data['EmailAddress']) is True:
            print('User already exists in DB!')

    def test_confirm_email_address_via_link(self):
        user_info = self.user.end_to_end_registration_user_data
        confirmation = self.user.confirm_email(user_info['EmailConfirmationCode'], user_info['id'])
        user_info_after = self.user.get_info_about_user(self.user.user_data['EmailAddress'])

        assert 0 == user_info['IsEmailConfirmed']
        assert True is self.check_success_status(confirmation)
        assert 1 == user_info_after['IsEmailConfirmed']
        assert None is user_info_after['EmailConfirmationCode']

    def test_create_legal_entity_organization(self):
        organization_creator = User(self.user.end_to_end_registration_user_data['UserName'],
                                    data=self.user.end_to_end_registration_user_data)
        assert True is organization_creator.is_can_organization_create
        organization = Organization(organization_creator)

        x = organization.generate_random_data('Юридична особа', selected_kind=3)
        print(x)
        self.created_organization = organization.update_or_create_organization(x)
        print(self.created_organization)

        assert False is organization_creator.is_can_organization_create
        assert str(self.created_organization['identifier']['apiId']) == x['code_of_organization']
        assert True is organization.is_organization_registered(x['code_of_organization'])
