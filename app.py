from flask import Flask, request
from parameters.databasemanager import DatabaseManager
from parameters.credentials import db_name_app, uri_app, db_name_plant, uri_plant
from db_classes.classes_si_db.user import User
from db_classes.classes_si_db.hubgroup import HubGroup
from db_classes.classes_si_db.exceptions import UserCreationException, ObjectCreationException
from utilities.object_creation_utilities import create_group_and_assign_to_user, create_hub_and_assign_to_group
from utilities.object_management_utilities import delete_user, delete_hub, delete_group
from utilities.common import UserMustLoggedException
from utilities.object_creation_utilities import Hub

app = Flask(__name__)

db = DatabaseManager(db_name=db_name_app, uri=uri_app)
db.connect_db()

plants_db = DatabaseManager(db_name=db_name_plant, uri=uri_plant)
plants_db.connect_db()


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
    # TODO
    pass


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    try:
        User.create_user(username, password)
    except UserCreationException as e:
        return throw_error_page(e.message)
    login_user()
    return  # TODO return SOMETHING here (idk, a page, something like that)


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
    group = HubGroup.objects(u_id=group_id).first()
    if not group:
        return throw_error_page("Specified group does not exist")
    try:
        if name:
            create_hub_and_assign_to_group(group=group, hub_name=name)
        else:
            create_hub_and_assign_to_group(group=group)
    except ObjectCreationException as e:
        return throw_error_page(e.message)
    return  # TODO return a proper page even here, idk something like "yea! you created the hub!"


@app.route('/unregister_user', methods=['POST'])
def unregister_user():
    if not user_is_logged_in():
        return throw_error_page("User should logged in")
    user = User.objects(u_id=get_uid_from_cookies()).first()
    delete_user(user)
    return # TODO "You've successfully unsubscribed yourself"

@app.route('/unregister_group', methods=['POST'])
def unregister_user():
    data = request.get_json()
    if not user_is_logged_in():
        return throw_error_page("User should logged in")
    group_id = data['group_id']
    if not group_id:
        return throw_error_page("Unspecified group id")
    group = HubGroup.objects(u_id=group_id).first()
    delete_group(group)
    return # TODO "You've successfully unsubscribed the hubgroup with name (groupname)"


@app.route('/unregister_hub', methods=['POST'])
def unregister_user():
    data = request.get_json()
    if not user_is_logged_in():
        return throw_error_page("User should logged in")
    hub_id = data['hub_id']
    if not hub_id:
        return throw_error_page("Unspecified hub id")
    hub = Hub.objects(u_id=hub_id).first()
    delete_hub(hub)
    eturn  # TODO "You've successfully unsubscribed the hub with name (hubname)"



@app.route('/login', methods=['POST'])
def login_user():
    """
    A function to login the user, manage the cookie (generate them, and so on)
    """
    raise NotImplemented()


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
