from mongoengine import EmbeddedDocument
from mongoengine import StringField, ListField, EmbeddedDocumentField, BooleanField, DateTimeField, FloatField
from bson import json_util
import json
from datetime import datetime


class Measure(EmbeddedDocument):
    name = StringField(required=True)
    date = DateTimeField(default=datetime.utcnow)
    value = FloatField(required=True)
    unit_of_measure = StringField(required=True)


class Sensor(EmbeddedDocument):
    name = StringField(required=True)
    description = StringField()
    measures = ListField(EmbeddedDocumentField(Measure))
