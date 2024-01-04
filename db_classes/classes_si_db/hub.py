from mongoengine import Document, StringField, DictField, DateTimeField, FloatField, EnumField, ListField
from mongoengine import EmbeddedDocumentField
from measures import Sensor
from bson import json_util
from ..common import WateringInterval
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

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))
