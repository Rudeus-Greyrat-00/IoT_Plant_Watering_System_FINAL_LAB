from mongoengine import Document, StringField, DictField, DateTimeField, ListField, ReferenceField, SequenceField
from mongoengine import GeoPointField
from .hubs import Hubs
from bson import json_util
import json
import datetime
from .classes_si_db_common import object_name_max_length, validate_object_name
from .classes_si_db_common import InvalidObjectNameException, ObjectNameTooLongException


class HubGroups(Document):
    u_id = SequenceField(collection_name='Groups')

    name = StringField()
    creation_date = DateTimeField()
    location = GeoPointField(required=True)

    hubs = ListField(ReferenceField(Hubs))
    additional_attributes = DictField()
    meta = {'collection': 'Groups'}

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))

    @classmethod
    def create_group(cls, location, name="Unnamed group"):
        if not validate_object_name(name):
            raise InvalidObjectNameException()
        if len(name) > object_name_max_length:
            raise ObjectNameTooLongException(name)
        return HubGroups._loc_create_group(name=name, location=location)

    @classmethod
    def _loc_create_group(cls, location, name="Unnamed group"):
        group = cls(name=name, location=location, date=datetime.date.today())
        group.save()
        return group
