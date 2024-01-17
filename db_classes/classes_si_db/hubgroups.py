from mongoengine import Document, StringField, DictField, DateTimeField, ListField, ReferenceField
from .hubs import Hubs
from bson import json_util
import json
import datetime
from .classes_si_db_common import object_name_max_length, validate_object_name
from .classes_si_db_common import InvalidObjectNameException, ObjectNameTooLongException


class HubGroups(Document):
    u_id = StringField(required=True)  # assigned in production

    name = StringField()
    creation_date = DateTimeField()

    hubs = ListField(ReferenceField(Hubs))
    additional_attributes = DictField()
    meta = {'collection': 'Groups'}

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))

    @classmethod
    def create_group(cls, name="Unnamed group"):
        if not validate_object_name(name):
            raise InvalidObjectNameException()
        if len(name) > object_name_max_length:
            raise ObjectNameTooLongException(name)
        groups = HubGroups.objects.order_by('u_id')
        current = 0
        for group in groups:
            if group.u_id == str(current):
                current += 1
            else:
                break
        return HubGroups._loc_create_group(u_id=current, name=name)

    @classmethod
    def _loc_create_group(cls, u_id, name="Unnamed group"):
        group = cls(u_id=u_id, name=name, date=datetime.date.today())
        group.save()
        return group
