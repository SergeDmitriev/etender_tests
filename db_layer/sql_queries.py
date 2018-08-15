# region Users
def select_where_email_equal(email_address):
    return 'select * from AbpUsers where EmailAddress = \'{0}\''.format(email_address)


# endregion Users
