from mongoengine import Document, StringField, DictField, DateTimeField, ListField, ReferenceField
from hub import Hub
from bson import json_util
import json


class HubGroup(Document):
    u_id = StringField(required=True)  # assigned in production

    name = StringField()
    creation_date = DateTimeField()

    hubs = ListField(ReferenceField(Hub))
    additional_attributes = DictField()
    meta = {'collection': 'Groups'}

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return json.loads(json_util.dumps(data))
