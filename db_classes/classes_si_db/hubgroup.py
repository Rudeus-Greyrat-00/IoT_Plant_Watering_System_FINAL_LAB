from mongoengine import Document, StringField, DictField, DateTimeField, ListField, ReferenceField
from hub import Hub
from bson import json_util
import json
import datetime


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

    @classmethod
    def create_group(cls, u_id, name="Unnamed group"):
        group = cls(u_id=u_id, name=name, date=datetime.date.today())
        group.save()
        return group
