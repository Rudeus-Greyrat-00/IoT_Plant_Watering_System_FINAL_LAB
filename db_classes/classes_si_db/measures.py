from mongoengine import EmbeddedDocument
from mongoengine import StringField, ListField, EmbeddedDocumentField, BooleanField, DateTimeField, FloatField
from bson import json_util
import json
from datetime import datetime


class Measure(EmbeddedDocument):
    name = StringField(required=True)
    date = DateTimeField(default=datetime.now())
    value = FloatField(required=True)
    unit_of_measure = StringField(required=True)

    @classmethod
    def create_measure(cls, name, value, unit_of_measure):
        return cls(name=name, date=datetime.now(), value=value,
                   unit_of_measure=unit_of_measure)
