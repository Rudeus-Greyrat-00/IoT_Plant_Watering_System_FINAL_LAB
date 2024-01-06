import string
from hashlib import sha256

password_max_length = 50
username_max_length = 25
object_name_max_length = 50
password_enabled_characters = string.printable
username_additional_characters = "_-."
username_enabled_characters = string.ascii_letters + string.digits + username_additional_characters

object_name_additional_characters = "_-."
object_name_enabled_characters = string.ascii_letters + string.digits + object_name_additional_characters


def validate_password(password: str):
    for c in password:
        if c not in password_enabled_characters:
            return False
    return True


def validate_username(username: str):
    for c in username:
        if c not in username_enabled_characters:
            return False
    return True


def validate_object_name(object_name: str):
    for c in object_name:
        if c not in object_name_enabled_characters:
            return False
    return True


def hash_string(str_var: str):
    return sha256(str_var.encode('utf-8'))


class ObjectCreationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__("An error occurred when creating an object:\n" + self.message)


class ObjectNameTooLongException(ObjectCreationException):
    def __init__(self, object_name):
        self.message = ("The name of the object is too long (max length: " + str(object_name_max_length) +
                        ", actual length: " + str(len(object_name)) + ")")
        super().__init__(self.message)


class InvalidObjectNameException(ObjectCreationException):
    def __init__(self, message=None):
        if message is None:
            self.message = ("The object name can contains only letters, numbers and "
                            + object_name_additional_characters)
        else:
            self.message = message
        super().__init__(self.message)


class UserCreationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidPasswordException(UserCreationException):
    def __init__(self, password, message="The password contains invalid characters"):
        invalid_characters = ""
        for c in password:
            if c not in password_enabled_characters:
                invalid_characters += c
        if len(invalid_characters) > 0:
            self.message = message + ": " + invalid_characters
        else:
            self.message = message
        super().__init__(self.message)


class InvalidUsernameException(UserCreationException):
    def __init__(self, message=None):
        if message is None:
            self.message = "The username can contains only letters, numbers and " + username_additional_characters
        else:
            self.message = message
        super().__init__(self.message)


class PasswordTooLongException(UserCreationException):
    def __int__(self, password: str):
        self.message = ("The password is too long (max length: " + str(password_max_length) +
                        ", actual length: " + str(len(password)) + ")")
        super().__init__(self.message)


class UsernameTooLongException(UserCreationException):
    def __int__(self, username: str):
        self.message = ("The username is too long (max length: " + str(username_max_length) +
                        ", actual length: " + str(len(username)) + ")")
        super().__init__(self.message)


class UserExistException(UserCreationException):
    def __int__(self, username):
        self.message = "Username " + username + " already exist!"
        super().__init__(self.message)


class UserNotExistException(Exception):
    def __int__(self, username):
        self.message = "Username " + username + " does not exist!"
        super().__init__(self.message)
