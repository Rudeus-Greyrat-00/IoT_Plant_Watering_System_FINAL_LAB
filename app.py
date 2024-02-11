from flask import Flask, request, render_template, url_for, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user
from parameters.databasemanager import DatabaseManager
from mongoengine.errors import DoesNotExist
from parameters.credentials import db_name_app, uri_app, db_name_plant, uri_plant
from db_classes.classes_si_db.user import Users, UserObject
from db_classes.classes_si_db.smartpots import SmartPots
from db_classes.classes_si_db.measures import Measure
from db_classes.classes_si_db.exceptions import UserCreationException, ObjectCreationException
from db_classes.classes_si_db.classes_si_db_common import ObjectModifyException
from db_classes.common import WateringFrequency, get_watering_frequency_choices
from utilities.object_creation_utilities import create_pot_and_assign_to_user
from utilities.object_management_utilities import delete_user, delete_pot
from utilities.common import UserMustLoggedException
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.new_smart_pot_form import NewSmartPotForm
from external_services.location_service.location import search_address
from external_services.location_service.location import search_coordinates
from external_services.plant_details_service.plants import get_species_common_names, get_species_fields
from external_services.weather_service.weather import get_current_weather
import random
import ast
import paho.mqtt.client as mqtt
from utilities.common import get_current_time
import string
import os
import requests

app_mode = 'DEBUG'

login_manager = LoginManager()
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager.init_app(app)

secret_string = 'smartpot_9459019280'

db = DatabaseManager(db_name=db_name_app, uri=uri_app)
db.connect_db(alias="default")

plants_db = DatabaseManager(db_name=db_name_plant, uri=uri_plant)
plants_db.connect_db(alias="plants")


# ---- MQTT ---- #
# MQTT Callback
def on_message(client, userdata, message):
    dictionary = ast.literal_eval(message.payload.decode("utf-8"))
    serial_number = dictionary["serial_number"]
    try:
        pot = SmartPots.objects(serial_number=serial_number).first()
    except DoesNotExist:
        return

    pot.add_measure("Soil Humidity", dictionary['soil_humidity'], "%")
    pot.add_measure("Air Humidity", dictionary['air_humidity'], "%")
    pot.add_measure("Air Temperature", dictionary['air_temperature'], "°C")
    pot.add_measure("Light", dictionary['light'], "%")


# Set up MQTT client
client_ID = ''.join(random.choice(string.digits) for i in range(6))
client = mqtt.Client(client_ID)
client.on_message = on_message
client.connect("broker.mqttdashboard.com", 1883, 60)
client.subscribe(f"{secret_string}/measurements")
client.loop_start()


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


def generate_settings_payload(pot: SmartPots):
    latitude, longitude = search_coordinates(pot.location)
    hour, minute = get_current_time(latitude, longitude)
    payload = str(dict(watering_frequency=pot.watering_frequency,
                       desired_humidity=pot.desired_humidity,
                       current_hour=hour,
                       current_minute=minute))
    return payload


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


@app.route('/register_pot', methods=['GET', 'POST'])
def register_pot():
    form = NewSmartPotForm()
    if user_is_logged_in():
        watering_frequency_choices = get_watering_frequency_choices()
        form.watering_frequency.choices = watering_frequency_choices
        if request.method == 'GET':
            return render_template('register_pot.html', form=form)
        elif request.method == 'POST':
            if form.validate_on_submit():
                name = form.name.data
                serial_number = form.serial_number.data
                location = form.location.data
                plant_name = form.plant_name.data
                desired_humidity = form.desired_humidity.data
                watering_frequency = form.watering_frequency.data
                additional_attributes = get_species_fields(plant_name)

                user_id = get_uid_from_cookies()  # from cookies
                user = Users.objects(u_id=user_id).first()
                try:
                    if name:
                        create_pot_and_assign_to_user(user=user, serial_number=serial_number, location=location,
                                                      plant_name=plant_name, desired_humidity=desired_humidity,
                                                      watering_frequency=watering_frequency,
                                                      additional_attributes=additional_attributes, pot_name=name)
                    else:
                        create_pot_and_assign_to_user(user=user, serial_number=serial_number, location=location,
                                                      plant_name=plant_name, desired_humidity=desired_humidity,
                                                      watering_frequency=watering_frequency,
                                                      additional_attributes=additional_attributes)
                    return render_template('register_pot.html', form=form,
                                           watering_frequency=watering_frequency_choices,
                                           success="Pot successfully registered")
                except ObjectCreationException as error:
                    return render_template("register_pot.html", form=form,
                                           error=error.message)
    else:
        return render_template("login.html")


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    locations = search_address(query)
    return jsonify(locations)


@app.route('/autocomplete_plant', methods=['GET'])
def autocomplete_plant():
    query = request.args.get('query')
    plants = get_species_common_names(query)
    return jsonify(plants)


@app.route('/unregister_user', methods=['GET'])
def unregister_user():
    if not user_is_logged_in():
        return throw_error_page("User should logged in")
    user = Users.objects(u_id=get_uid_from_cookies()).first()
    delete_user(user)
    return render_template("index.html")


@app.route('/unregister_pot/<int:pot_id>', methods=['GET'])
def unregister_pot(pot_id):
    if not user_is_logged_in():
        return throw_error_page("User should logged in")

    user = Users.objects(u_id=get_uid_from_cookies()).first()
    for pot in user.pots:
        if pot.u_id == pot_id:
            delete_pot(pot)
            deleted_pot = 1
            return render_template("smart_pots.html")

    return throw_error_page("Pot not Found")


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


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if user_is_logged_in():
        return render_template("dashboard.html")
    else:
        return render_template("login.html")


@app.route('/smart_pots', methods=['GET'])
def smart_pots():
    if user_is_logged_in():
        pots = Users.objects(username=current_user.username).first().pots
        return render_template("smart_pots.html", pots=pots)
    else:
        return render_template("login.html")


@app.route('/pot_details/<int:pot_id>', methods=['GET'])
def pot_details(pot_id):
    if user_is_logged_in():
        pot = SmartPots.objects(u_id=pot_id).first()
        user = Users.objects(username=current_user.username).first()

        for user_pot in user.pots:
            if user_pot.u_id == pot_id:
                pot_det = user_pot
                latitude, longitude = search_coordinates(pot_det.location)
                weather_object = get_current_weather(latitude, longitude)

                return render_template('pot.html', pot=pot_det, latitude=latitude, longitude=longitude,
                                       weather_object=weather_object)

        return throw_error_page("Not found")
    else:
        return render_template("login.html")


@app.route('/modify_pot_details/<int:pot_id>', methods=['GET', 'POST'])
def modify_pot_details(pot_id):
    if user_is_logged_in():
        form = NewSmartPotForm()
        if request.method == 'GET':
            watering_frequency_choices = get_watering_frequency_choices()
            form.watering_frequency.choices = watering_frequency_choices
            user = Users.objects(username=current_user.username).first()
            for user_pot in user.pots:
                if user_pot.u_id == pot_id:
                    pot_det = user_pot
                    form.name.data = pot_det.name
                    form.serial_number.data = pot_det.serial_number
                    form.location.data = pot_det.location
                    form.plant_name.data = pot_det.plant_name
                    form.desired_humidity.data = pot_det.desired_humidity
                    form.watering_frequency.data = pot_det.watering_frequency
                    return render_template("modify_pot_details.html", form=form)
        elif request.method == 'POST':
            watering_frequency_choices = get_watering_frequency_choices()
            form.watering_frequency.choices = watering_frequency_choices
            user = Users.objects(username=current_user.username).first()
            name = form.name.data
            location = form.location.data
            plant_name = form.plant_name.data
            desired_humidity = form.desired_humidity.data
            watering_frequency = form.watering_frequency.data
            additional_attributes = get_species_fields(plant_name)
            try:
                for user_pot in user.pots:
                    if user_pot.u_id == pot_id:
                        pot_det = user_pot
                        pot_det.name = name
                        pot_det.location = location
                        pot_det.plant_name = plant_name
                        pot_det.desired_humidity = float(desired_humidity)
                        pot_det.watering_frequency = watering_frequency
                        pot_det.additional_attributes = additional_attributes
                        pot_det.save()

                        client.publish(f"{secret_string}/update_pot_setting/{pot_det.serial_number}",
                                       generate_settings_payload(pot_det))
                        return render_template("modify_pot_details.html", form=form,
                                               success="Pot successfully registered")
            except ObjectModifyException as e:
                return render_template("modify_pot_details.html", form=form, error=e.message)
    else:
        return render_template("index.html")


@app.route('/authorize_watering/<string:serial_number>', methods=['GET'])
def authorize_watering(serial_number):
    try:
        pot = SmartPots.objects(serial_number=serial_number).first()
    except DoesNotExist:
        return "Not Found", 404
    if pot is None:
        return "Not Found", 404

    latitude, longitude = search_coordinates(pot.location)
    weather = get_current_weather(latitude, longitude)

    if weather.weather != "Clear":
        return "Unauthorized", 200

    return "Authorized", 200


@app.route('/get_settings/<string:serial_number>', methods=['GET'])
def get_pot_settings(serial_number):
    try:
        pot = SmartPots.objects(serial_number=serial_number).first()
    except DoesNotExist:
        return "Not Found", 404
    if pot is None:
        return "Not Found", 404

    return generate_settings_payload(pot), 200


# ----- TERRAIN SCORING PARAMETER ----- #
@app.route('/get_terrain_score/<string:serial_number>', methods=['GET'])
def get_terrain_score(serial_number):
    pass

# ----- POTENTIAL FAULT DETECTION ----- #
@app.route('/detect_fault/<string:serial_number>', methods=['GET'])
def detect_fault(serial_number):
    pass

# ----- DATA REPRESENTATION ----- #
@app.route('/chart', methods=['GET'])
def chart():
    pass


if __name__ == '__main__':
    app.run()
