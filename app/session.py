

'''
AuthenticatedAdminSession class to represent
a valid authenticated admin session. This class is used to ensure that
only properly authenticated admin users can access admin functionalities.
Previous dict implentaion allowed forgery of admin sessions.

'''
class AuthenticatedAdminSession:
    def __init__(self, user_dict):
        self.id = user_dict.get("id") # added line
        self.username = user_dict.get("username") # added line
        self.is_admin = user_dict.get("is_admin", False) # ensure default to False
        self._valid = True  # internal flag to mark session validity

    def is_valid(self):
        return self._valid and self.is_admin # must be admin and valid


