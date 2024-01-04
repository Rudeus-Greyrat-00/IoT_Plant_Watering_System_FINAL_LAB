from mongoengine import Document, StringField, FloatField, EnumField
from bson import json_util
from ..common import WateringInterval
import json


class Plant(Document):
    name = StringField(required=True)
    description = StringField()

    ideal_humidity = FloatField(required=True)
    ideal_watering = EnumField(WateringInterval, required=True)
    ideal_air_temperature = FloatField(required=True)

    meta = {'collection': 'Plants'}

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))
