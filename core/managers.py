class UserBaseManager(object):
    def __init__(self, base_role, base_username, user_password):
        self.role = base_role
        self.username = base_username
        self.password = user_password

    def return_spec_page(self):
        pass


class OwnerManager(UserBaseManager):
    def __init__(self, role, username, password):
        UserBaseManager.__init__(self, role, username, password)


    def return_spec_page(self):
        pass



# class BaseViewerManager(UserBaseManager):
#     def __init__(self, role, username, password):
#         UserBaseManager.__init__(self, base_role, username, password)
#
#     def return_spec_page(self):
#         pass



# viewer = BaseViewerManager("viewer", "case7", "Qq123456")