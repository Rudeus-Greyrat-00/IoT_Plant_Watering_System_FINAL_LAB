from db_classes.classes_si_db.user import Users
from db_classes.classes_si_db.hubgroups import HubGroups
from hashlib import sha256


def hash_string(str_var: str):
    return sha256(str_var.encode('utf-8'))


class UserMustLoggedException(Exception):
    def __init__(self, message):
        if message is not None:
            self.message = "To perform this action: " + message + "user must logged in!"
        else:
            self.message = "User must logged in to perform such an action"
        super().__init__(self.message)
