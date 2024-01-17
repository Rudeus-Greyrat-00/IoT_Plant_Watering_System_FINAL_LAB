from flask import Flask, request, render_template, url_for, jsonify
from flask_login import LoginManager
from parameters.databasemanager import DatabaseManager
from parameters.credentials import db_name_app, uri_app, db_name_plant, uri_plant
from db_classes.classes_si_db.user import Users, UserObject
from db_classes.classes_si_db.hubgroups import HubGroups
from db_classes.classes_si_db.exceptions import UserCreationException, ObjectCreationException
from utilities.object_creation_utilities import create_group_and_assign_to_user, create_hub_and_assign_to_group
from utilities.object_management_utilities import delete_user, delete_hub, delete_group
from utilities.common import UserMustLoggedException
from utilities.object_creation_utilities import Hubs
import random
import string

login_manager = LoginManager()
app = Flask(__name__)

app.secret_key = ''.join(random.choices(string.printable, k=20))

login_manager.init_app(app)

db = DatabaseManager(db_name=db_name_app, uri=uri_app)
db.connect_db()

plants_db = DatabaseManager(db_name=db_name_plant, uri=uri_plant)
plants_db.connect_db()


@login_manager.user_loader
def load_user(user_id):
    if not Users.user_exist_uid(user_id):
        return None
    return UserObject(Users.objects(u_id=user_id).first())


def user_is_logged_in():  # more parameters may be necessary
    """
    A function that check if the user sending the request is logged in or not
    :return: true if the user is logged in, false otherwise
    """
    raise NotImplemented()


def get_uid_from_cookies():  # more parameters may be necessary
    """
    A function used to get the user id of a logged in user sending a request.
    :return: the user id of the logged user that is sending the request
    """
    if not user_is_logged_in():
        raise UserMustLoggedException("The user shall be logged in!")
    # TODO get user id from cookie
    raise NotImplemented()


def throw_error_page(error_str: str):
    """
    A function to return a generic error page
    :param error_str: an error message that it may be better to not show to the final user,
    perhaps discard it in production (though they might still be rather useful during debug!!)
    :return: it returns a properly formatted, cute and well put together error page
    """
    raise NotImplemented()
    pass


@app.route('/', methods=['GET'])
def homepage():
    return render_template("index.html")


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == "POST":
        data = request.get_json()
        try:
            user = User.create_user(
                username=data.get('username'),
                password=data.get('password')
            )
            return jsonify(user.to_dict()), 201
        except UserCreationException as e:
            return jsonify({'error': str(e.message)}), 400
    elif request.method == "GET":
        return render_template("register.html")

    """
    if request.method == "POST":
        data = request.get_json()
        username = data['username']
        password = data['password']
        try:
            user = User.create_user(username, password)
            return jsonify(user.to_dict()), 201
            #login_user()
        except UserCreationException as e:
            return throw_error_page(e.message)
    elif request.method == "GET":
        return render_template("register.html")
    """


@app.route('/register_group', methods=['POST'])
def registrate_group():
    data = request.get_json()
    name = data['name']
    if not user_is_logged_in():
        throw_error_page("User must be logged in")
        return
    user_id = get_uid_from_cookies()  # from cookies
    user = User.objects(u_id=user_id).first()
    try:
        if name:
            create_group_and_assign_to_user(user=user, group_name=name)
        else:
            create_group_and_assign_to_user(user=user)
    except ObjectCreationException as e:
        return throw_error_page(e.message)


@app.route('/register_hub', methods=['POST'])
def registrate_hub():
    data = request.get_json()
    group_id = data['group_id']
    name = data['name']
    if not user_is_logged_in():
        return throw_error_page("User must be logged in")
    elif not group_id:
        return throw_error_page("Unspecified group id")
    group = HubGroups.objects(u_id=group_id).first()
    if not group:
        return throw_error_page("Specified group does not exist")
    try:
        if name:
            create_hub_and_assign_to_group(group=group, hub_name=name)
        else:
            create_hub_and_assign_to_group(group=group)
    except ObjectCreationException as e:
        return throw_error_page(e.message)
    return render_template("index.html")


@app.route('/unregister_user', methods=['POST'])
def unregister_user():
    if not user_is_logged_in():
        return throw_error_page("User should logged in")
    user = User.objects(u_id=get_uid_from_cookies()).first()
    delete_user(user)
    return render_template("index.html")


@app.route('/unregister_group', methods=['POST'])
def unregister_group():
    data = request.get_json()
    if not user_is_logged_in():
        return throw_error_page("User should logged in")
    group_id = data['group_id']
    if not group_id:
        return throw_error_page("Unspecified group id")
    group = HubGroups.objects(u_id=group_id).first()
    delete_group(group)
    return render_template("index.html")


@app.route('/unregister_hub', methods=['POST'])
def unregister_hub():
    data = request.get_json()
    if not user_is_logged_in():
        return throw_error_page("User should logged in")
    hub_id = data['hub_id']
    if not hub_id:
        return throw_error_page("Unspecified hub id")
    hub = Hub.objects(u_id=hub_id).first()
    delete_hub(hub)
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == "GET":
        return render_template("login.html")
    else:
        return throw_error_page(e.message)


@app.route('/report', methods=['GET'])
def create_report():
    """
    A function to generate a report webpage
    :return: a well put together report page
    """
    if not user_is_logged_in():
        return throw_error_page("User must be logged in!!!")
    raise NotImplemented()


if __name__ == '__main__':
    app.run()
