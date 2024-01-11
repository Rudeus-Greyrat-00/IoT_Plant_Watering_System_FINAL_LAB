from flask import Flask, request
from parameters.databasemanager import DatabaseManager
from parameters.credentials import db_name_app, uri_app, db_name_plant, uri_plant
from db_classes.classes_si_db.user import User
from db_classes.classes_si_db.hubgroup import HubGroup
from utilities.object_creation_utilities import UserCreationException, ObjectCreationException
from utilities.object_creation_utilities import create_user, create_group
from utilities.object_management_utilities import assign_group_to_user, assign_hub_to_group
from utilities.object_management_utilities import delete_user, delete_hub, delete_group
from utilities.common import UserMustLoggedException

app = Flask(__name__)

db = DatabaseManager(db_name=db_name_app, uri=uri_app)
db.connect_db()

plants_db = DatabaseManager(db_name=db_name_plant, uri=uri_plant)
plants_db.connect_db()


def user_is_logged_in():
    # TODO check for cookie
    raise NotImplemented()

def get_uid():
    # TODO get user id from cookie
    raise NotImplemented()


def throw_error_page(error_str: str):
    # TODO uhm... everything, show a page with the error string, or even better a page with a generic error
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


@app.route('/create_group')
def generate_group():
    data = request.get_json()
    name = data['name']
    if not user_is_logged_in():
        throw_error_page("User must be logged in")
        return
    user_id = get_uid()
    if name:
        group = create_group(name)
    else:
        group = create_group()
    assign_group_to_user(group, user_id)




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


if __name__ == '__main__':
    app.run()
