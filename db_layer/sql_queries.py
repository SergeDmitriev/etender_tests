# region Users
def select_where_email_equal(email_address):
    return 'select * from AbpUsers where EmailAddress = \'{0}\''.format(email_address)


def select_email_confirmation_code(user_id):
    return 'select EmailConfirmationCode from AbpUsers where id = {0}'.format(user_id)


def select_is_email_confirmed(user_id):
    return 'select IsEmailConfirmed from AbpUsers where id = {0}'.format(user_id)
# endregion Users


# region OrganizationExts
def select_code_of_organization(org_code):
    return 'select top 1 CodeOfOrganization from OrganizationExts where CodeOfOrganization = \'{0}\''.format(str(org_code))
# endregion OrganizationExts
