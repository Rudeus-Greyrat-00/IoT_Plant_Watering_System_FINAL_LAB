from mongoengine import Document, StringField, DictField, DateTimeField, ListField, ReferenceField
from hubgroup import HubGroup
from bson import json_util
import json


class User(Document):
    u_id = StringField(required=True)  # assigned in production
    username = StringField(required=True)
    hashed_password = StringField(required=True)
    creation_date = DateTimeField()

    groups = ListField(ReferenceField(HubGroup))
    additional_attributes = DictField()
    meta = {'collection': 'Users'}

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))

