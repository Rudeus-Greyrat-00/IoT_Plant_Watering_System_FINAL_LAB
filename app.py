from flask import Flask, request, jsonify
from parameters.databasemanager import DatabaseManager
from parameters.credentials import db_name_app, uri_app, db_name_plant, uri_plant
from db_classes.common import WateringInterval
from db_classes.classes_si_db.user import User
from utility import hash_string, validate_password, validate_username
from utility import password_max_length, username_max_length
from utility import UserExistException, UserNotExistException, UserCreationException
from utility import InvalidPasswordException, InvalidUsernameException
from utility import PasswordTooLongException, UsernameTooLongException

app = Flask(__name__)

db = DatabaseManager(db_name=db_name_app, uri=uri_app)
db.connect_db()

plants_db = DatabaseManager(db_name=db_name_plant, uri=uri_plant)
plants_db.connect_db()


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


def create_user(username: str, password: str):
    if not validate_username(username):
        raise InvalidUsernameException()
    if len(username) > username_max_length:
        raise UsernameTooLongException(username)
    if not validate_password(password):
        raise InvalidPasswordException(password)
    if len(password) > password_max_length:
        raise PasswordTooLongException(password)
    if user_exist(username):
        raise UserExistException(username)
    users = User.objects.order_by('u_id')
    current = 0
    for user in users:
        if user.u_id == str(current):
            current += 1
        else:
            break
    User.create_user(u_id=current, username=username, hashed_password=hash_string(password))


def throw_error_page(error_str : str):
    # TODO
    pass

@app.route('/')
def homepage():
    # TODO
    pass


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    try:
        create_user(username, password)
    except UserCreationException as e:
        throw_error_page(e.message)
    login_user()


@app.route('/login', methods=['POST'])
def login_user():
    # TODO I don't know how to deal with cookies......
    pass


@app.route('/report', methods=['GET'])
def create_report():
    # TODO if user not loggeed in show an error

    # TODO acccess the db
    # TODO accesss measurements
    # render template.....
    pass


# @app.route('/create_group')

if __name__ == '__main__':
    app.run()
