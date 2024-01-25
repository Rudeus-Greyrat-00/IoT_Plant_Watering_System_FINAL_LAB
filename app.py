from flask import Flask, request, render_template, url_for, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user
from parameters.databasemanager import DatabaseManager
from parameters.credentials import db_name_app, uri_app, db_name_plant, uri_plant
from db_classes.classes_si_db.user import Users, UserObject
from db_classes.classes_si_db.hubgroups import HubGroups
from db_classes.classes_si_db.exceptions import UserCreationException, ObjectCreationException
from db_classes.common import WateringInterval
from utilities.object_creation_utilities import create_group_and_assign_to_user, create_hub_and_assign_to_group
from utilities.object_management_utilities import delete_user, delete_hub, delete_group
from utilities.common import UserMustLoggedException
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.new_hub_group import NewHubGroupForm
from forms.new_hub import NewHubForm
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
            login_user(UserObject(user))
            return render_template('dashboard.html')
        except UserCreationException as error:
            return render_template('register.html', form=form, error=error.message)

    return render_template('register.html', form=form)


@app.route('/register_group', methods=['GET', 'POST'])
def registrate_group():
    form = NewHubGroupForm()
    if user_is_logged_in():
        if request.method == 'GET':
            return render_template('register_hub_group.html', form=form)
        elif request.method == 'POST':
            if form.validate_on_submit():
                name = form.name.data
                location = form.location.data
                user_id = get_uid_from_cookies()  # from cookies
                user = Users.objects(u_id=user_id).first()
                try:
                    if name:
                        create_group_and_assign_to_user(user=user, location=location, group_name=name)
                    else:
                        create_group_and_assign_to_user(user=user, location=location)
                    return render_template('register_hub_group.html', form=form, success="Hub group successfully "
                                                                                         "registered")
                except ObjectCreationException as error:
                    return render_template("register_hub_group.html", form=form, error=error.message)
    else:
        return render_template("login.html")


@app.route('/register_hub/<int:hub_group_id>', methods=['GET', 'POST'])
def registrate_hub(hub_group_id):
    form = NewHubForm()
    if user_is_logged_in():
        if request.method == 'GET':
            watering_interval = WateringInterval
            return render_template('register_hub.html', form=form, watering_interval=watering_interval)
        elif request.method == 'POST':
            if form.validate_on_submit():
                name = form.name.data
                desired_humidity = form.desired_humidity.data
                watering_frequency = request.form.get('select_option')
                group = HubGroups.objects(u_id=hub_group_id).first()
                try:
                    if name:
                        create_hub_and_assign_to_group(group=group, desired_humidity=desired_humidity,
                                                       watering_frequency=int(watering_frequency), hub_name=name)
                    else:
                        create_hub_and_assign_to_group(group=group)
                    return render_template("register_hub.html", form=form, success="Hub successfully associated to the group.")
                except ObjectCreationException as e:
                    return render_template("hub_list.html", form=form, error=e.message)
    else:
        return render_template("login.html")


@app.route('/unregister_user', methods=['GET'])
def unregister_user():
    if not user_is_logged_in():
        return throw_error_page("User should logged in")
    user = Users.objects(u_id=get_uid_from_cookies()).first()
    delete_user(user)
    return render_template("index.html")


@app.route('/unregister_group/<int:hub_group_id>', methods=['GET'])
def unregister_group(hub_group_id):
    if not user_is_logged_in():
        return throw_error_page("User should logged in")

    user = Users.objects(u_id=get_uid_from_cookies()).first()

    for hub_group in user.groups:
        if hub_group.u_id == hub_group_id:
            delete_group(hub_group)
            return render_template("index.html")

    return throw_error_page("Hub Group not Found")


@app.route('/unregister_hub', methods=['GET'])
def unregister_hub():
    if not user_is_logged_in():
        return throw_error_page("User should logged in")

    user = Users.objects(u_id=get_uid_from_cookies()).first()
    group_id = request.args.get('group_id')
    hub_id = request.args.get('hub_id')
    found = False

    for user_group in user.groups:
        print(user_group.u_id)
        if user_group.u_id == int(group_id):
            found = True
            break

    if not found:
        return throw_error_page("Group not found")

    for current_hub in HubGroups.objects(u_id=group_id).first().hubs:
        if current_hub.u_id == int(hub_id):
            delete_hub(current_hub)
            return render_template('index.html') # Da Implementare

    return throw_error_page('Hub not found')



@app.route('/login', methods=['GET', 'POST'])
def endpoint_login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = Users.hash_string(form.password.data)
        remember = form.remember_me.data
        if Users.user_exist(username) and Users.objects(username=username).first().hashed_password == password:
            login_user(UserObject(Users.objects(username=username).first()), remember=remember)
            return render_template("dashboard.html")
        else:
            return render_template("login.html", form=form, error="Username or password not correct.")

    return render_template('login.html', form=form)


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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if user_is_logged_in():
        return render_template("dashboard.html")
    else:
        return render_template("login.html")

@app.route('/hub_groups', methods=['GET'])
def hub_groups():
    if user_is_logged_in():
        groups = Users.objects(username=current_user.username).first().groups
        return render_template("hub_groups.html", groups=groups)
    else:
        return render_template("login.html")

@app.route('/hub_list/<int:hub_group_id>', methods=['GET'])
def hub_list(hub_group_id):
    if user_is_logged_in():
        group = HubGroups.objects(u_id=hub_group_id).first()
        user = Users.objects(username=current_user.username).first()

        for user_group in user.groups:
            if user_group.u_id == hub_group_id:
                hubs = user_group.hubs
                return render_template("hub_list.html", group=group, hubs=hubs)

        return throw_error_page("Not found")

    else:
        return render_template("login.html")

@app.route('/hub/<int:hub_id>', methods=['GET'])
def hub():
    if user_is_logged_in():
        return render_template("hub.html")
    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run()
