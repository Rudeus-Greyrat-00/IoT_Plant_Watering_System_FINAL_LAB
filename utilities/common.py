from db_classes.classes_si_db.user import User
from db_classes.classes_si_db.hubgroup import HubGroup
from hashlib import sha256


def user_exist(username: str):
    user = User.objects(username=username).first()
    if user:
        return True
    return False


def user_exist_uid(u_id: str):
    user = User.objects(u_id=u_id).first()
    if user:
        return True
    return False


def hash_string(str_var: str):
    return sha256(str_var.encode('utf-8'))


class UserMustLoggedException(Exception):
    def __init__(self, message):
        if message is not None:
            self.message = "To perform this action: " + message + "user must logged in!"
        else:
            self.message = "User must logged in to perform such an action"
        super().__init__(self.message)
