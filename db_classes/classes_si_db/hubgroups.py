from mongoengine import Document, StringField, DictField, DateTimeField, ListField, ReferenceField, SequenceField,\
    EmbeddedDocument, EmbeddedDocumentField
from .hubs import Hubs
from bson import json_util
import json
import datetime
from .classes_si_db_common import object_name_max_length, validate_object_name
from .classes_si_db_common import InvalidObjectNameException, ObjectNameTooLongException


class HubGroups(EmbeddedDocument):
    u_id = SequenceField(collection_name='HubGroup')

    name = StringField()
    creation_date = DateTimeField()
    location = StringField(required=True)

    hubs = ListField(EmbeddedDocumentField(Hubs))
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
        group = cls(name=name, location=location)
        #group.save()
        return group
