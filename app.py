from flask import Flask, request, render_template, url_for, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user
from parameters.databasemanager import DatabaseManager
from parameters.credentials import db_name_app, uri_app, db_name_plant, uri_plant
from db_classes.classes_si_db.user import Users, UserObject
from db_classes.classes_si_db.hubgroups import HubGroups
from db_classes.classes_si_db.exceptions import UserCreationException, ObjectCreationException
from utilities.object_creation_utilities import create_group_and_assign_to_user, create_hub_and_assign_to_group
from utilities.object_management_utilities import delete_user, delete_hub, delete_group
from utilities.common import UserMustLoggedException
from forms.register_form import RegisterForm
from utilities.object_creation_utilities import Hubs
import random
import string
import os

app_mode = 'DEBUG'

login_manager = LoginManager()
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager.init_app(app)

db = DatabaseManager(db_name=db_name_app, uri=uri_app)
db.connect_db(alias="default")

plants_db = DatabaseManager(db_name=db_name_plant, uri=uri_plant)
plants_db.connect_db(alias="plants")


# ----- FLASK LOGIN CALLBACK ----- #

@login_manager.user_loader
def load_user(user_id):
    if not Users.user_exist_uid(user_id):
        return None
    return UserObject(Users.objects(u_id=user_id).first())


# ----- UTILITY FUNCTIONS ----- #

def user_is_logged_in():
    """
    A function that check if the user sending the request is logged in or not
    :return: true if the user is logged in, false otherwise
    """
    return current_user.is_authenticated


def get_uid_from_cookies():  # more parameters may be necessary
    """
    A function used to get the user id of a logged-in user sending a request.
    :return: the user id of the logged user that is sending the request
    """
    if not user_is_logged_in():
        raise UserMustLoggedException("The user shall be logged in!")
    return current_user.get_id()


def throw_error_page(error_str: str):
    """
    A function to return a generic error page
    :param error_str: an error message if in debug mode, a tidy cute generic error page otherwise
    :return: it returns a properly formatted, cute and well put together error page
    """
    if app_mode == 'DEBUG':
        return jsonify({'error': 'param: ' + error_str}), 400
    else:
        raise NotImplemented()  # TODO generic error page


# ----- ENDPOINTS ----- #

@app.route('/', methods=['GET'])
def homepage():
    return render_template("index.html")


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()  # POST
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = Users.create_user(username, password)
            login_user(user)
            return render_template('index.html', form=form)
        except UserCreationException as error:
            return render_template('register.html', form=form, error=error.message)

    return render_template('register.html', form=form)


@app.route('/register_group', methods=['POST'])
def registrate_group():
    data = request.get_json()
    name = data['name']
    location = data['location_service']
    if not user_is_logged_in():
        throw_error_page("User must be logged in")
        return
    user_id = get_uid_from_cookies()  # from cookies
    user = Users.objects(u_id=user_id).first()
    try:
        if name:
            create_group_and_assign_to_user(user=user, location=location, group_name=name)
        else:
            create_group_and_assign_to_user(user=user, location=location)
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
    user = Users.objects(u_id=get_uid_from_cookies()).first()
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
    hub = Hubs.objects(u_id=hub_id).first()
    delete_hub(hub)
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def endpoint_login_user():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form.get('username')
        password = Users.hash_string(request.form.get('password'))
        remember = bool(request.form.get('remember me'))
        if Users.user_exist(username) and Users.objects(username=username).first().hashed_password == password:
            login_user(UserObject(Users.objects(username=username).first()), remember=remember)
            return render_template("index.html")
        else:
            return render_template("login.html")  # TODO warning -- > username or password incorrect!


@app.route('/logout', methods=['GET'])
def endpoint_logout_user():
    if user_is_logged_in():
        logout_user()
    return render_template("index.html")


@app.route('/report', methods=['GET'])
def create_report():
    """
    A function to generate a report webpage
    :return: a well put together report page
    """
    if not user_is_logged_in():
        return throw_error_page("User must be logged in!!!")
    raise NotImplemented()


@app.route('/settings', methods=['GET', 'POST'])
def endpoint_objects_settings():
    if not user_is_logged_in():
        return render_template("index.html")
    if request.method == 'GET':
        return  # TODO page that allow to chose a group and an hub to change his settings, a form is necessary. From here the user can also SEE
    elif request.method == 'POST':  ## WE NEED TO FIGURE THIS OUT (some scripting may be necessary inside the page to get the group_id given the name of the group and the hub, and the UI must be
        user_id = get_uid_from_cookies()
        # something something we got the hub_id
        hub_id = request.values.get("hub_id")
        desired_humidity = request.values.get(
            "desired_humidity")  # set by the user OR chosed by a preset (again, this is something which is done from the page)
        watering_frequency = request.values.get("watering_frequency")

        hub = Hubs.objects(u_id=hub_id).first()
        hub.desired_humidity = desired_humidity
        hub.watering_frequency = watering_frequency
        hub.save()

        return  # TODO what do we return? A confirm page? The main setting page?


if __name__ == '__main__':
    app.run()
