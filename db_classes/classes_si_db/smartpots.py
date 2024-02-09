from mongoengine import Document, StringField, DictField, DateTimeField, ListField, ReferenceField, SequenceField,\
    EmbeddedDocument, EmbeddedDocumentField, GeoPointField, FloatField, EnumField, IntField
from ..common import WateringFrequency
from .measures import Sensor
from bson import json_util
import json
import datetime
from .classes_si_db_common import object_name_max_length, validate_object_name
from .classes_si_db_common import InvalidObjectNameException, ObjectNameTooLongException


class SmartPots(Document):
    u_id = SequenceField(collection_name='SmartPots')

    name = StringField()
    creation_date = DateTimeField()
    location = StringField(required=True)

    # Plant data
    plant_name = StringField()
    desired_humidity = FloatField()
    watering_frequency = IntField(required=True)

    # Sensor data
    sensors = ListField(EmbeddedDocumentField(Sensor))

    additional_attributes = DictField()
    meta = {'collection': 'SmartPots'}

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))

    @classmethod
    def create_pot(cls, location, plant_name, desired_humidity, watering_frequency, additional_attributes,
                   name="Unnamed group"):
        if not validate_object_name(name):
            raise InvalidObjectNameException()
        if len(name) > object_name_max_length:
            raise ObjectNameTooLongException(name)
        return SmartPots._loc_create_pot(name=name, location=location, plant_name=plant_name,
                                         desired_humidity=desired_humidity, watering_frequency=watering_frequency,
                                         additional_attributes=additional_attributes)

    @classmethod
    def _loc_create_pot(cls, location, plant_name, desired_humidity, watering_frequency, additional_attributes,
                        name="Unnamed group"):
        pot = cls(name=name, location=location, plant_name=plant_name, desired_humidity=desired_humidity,
                  watering_frequency=watering_frequency, additional_attributes=additional_attributes)
        pot.save()
        return pot
