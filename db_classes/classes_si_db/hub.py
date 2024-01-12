from mongoengine import Document, StringField, DictField, DateTimeField, FloatField, EnumField, ListField
from mongoengine import EmbeddedDocumentField
from measures import Sensor
from bson import json_util
import datetime
from ..common import WateringInterval
from classes_si_db_common import validate_object_name, object_name_max_length
from classes_si_db_common import InvalidObjectNameException, ObjectNameTooLongException
import json


class Hub(Document):
    u_id = StringField(required=True)  # assigned in production

    name = StringField()
    date = DateTimeField()
    additional_attributes = DictField()

    # Plant data
    desired_humidity = FloatField()
    watering_frequency = EnumField(WateringInterval, required=True)

    # Sensor data
    sensors = ListField(EmbeddedDocumentField(Sensor))

    meta = {'collection': 'Hubs'}

    @classmethod
    def create_hub(cls, name="Unnamed group"):
        if not validate_object_name(name):
            raise InvalidObjectNameException()
        if len(name) > object_name_max_length:
            raise ObjectNameTooLongException(name)
        groups = cls.objects.order_by('u_id')
        current = 0
        for group in groups:
            if group.u_id == str(current):
                current += 1
            else:
                break
        return cls._loc_create_hub(u_id=current, name=name)

    @classmethod
    def _loc_create_hub(cls, u_id, name="Unnamed group"):
        hub = cls(u_id=u_id, name=name, date=datetime.date.today())
        hub.save()
        return hub

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))
