from mongoengine import Document, StringField, DictField, DateTimeField, ListField, ReferenceField
from .hubgroup import HubGroup
from bson import json_util
from hashlib import sha256
import string
import json


password_max_length = 50
username_max_length = 25

password_enabled_characters = string.printable
username_additional_characters = "_-."
username_enabled_characters = string.ascii_letters + string.digits + username_additional_characters


class User(Document):
    u_id = StringField(required=True)  # assigned in production
    username = StringField(required=True)
    hashed_password = StringField(required=True)
    creation_date = DateTimeField()

    groups = ListField(ReferenceField(HubGroup))
    additional_attributes = DictField()
    meta = {'collection': 'Users'}

    @staticmethod
    def _validate_password(password: str):
        for c in password:
            if c not in password_enabled_characters:
                return False
        return True

    @staticmethod
    def _validate_username(username: str):
        for c in username:
            if c not in username_enabled_characters:
                return False
        return True

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))

    @classmethod
    def user_exist(cls, username: str):
        user = cls.objects(username=username).first()
        if user:
            return True
        return False

    @classmethod
    def user_exist_uid(cls, u_id: str):
        user = cls.objects(u_id=u_id).first()
        if user:
            return True
        return False

    @classmethod
    def _loc_create_user(cls, u_id, username, hashed_password):
        user = cls(u_id=u_id, username=username, hashed_password=hashed_password)
        user.save()
        return user

    @classmethod
    def create_user(cls, username: str, password: str):
        if not cls._validate_username(username):
            raise InvalidUsernameException()
        if len(username) > username_max_length:
            raise UsernameTooLongException(username)
        if not cls._validate_password(password):
            raise InvalidPasswordException(password)
        if len(password) > password_max_length:
            raise PasswordTooLongException(password)
        if cls.user_exist(username):
            raise UserExistException(username)
        users = User.objects.order_by('u_id')
        current = 0
        for user in users:
            if user.u_id == str(current):
                current += 1
            else:
                break
        return User._loc_create_user(u_id=current, username=username, hashed_password=sha256(password.encode('utf-8')))


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
