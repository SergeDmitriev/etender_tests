class UserBaseManager(object):
    def __init__(self, user_role, username, user_password):
        self.role = user_role
        self.username = username
        self.password = user_password

    def return_spec_page(self):
        pass


class BaseOwnerManager(UserBaseManager):
    def __init__(self, role, username, password):
        UserBaseManager.__init__(self, role, username, password)


class BaseViewerManager(UserBaseManager):
    pass


