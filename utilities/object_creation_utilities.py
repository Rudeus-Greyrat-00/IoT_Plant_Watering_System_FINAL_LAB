import string
from hashlib import sha256
from common import *
from db_classes.classes_si_db.user import User
from db_classes.classes_si_db.hubgroup import HubGroup
from db_classes.classes_si_db.hub import Hub

from object_management_utilities import assign_group_to_user, assign_hub_to_group


def create_group_and_assign_to_user(user: User, group_name: str = "Unnamed group"):
    hub_group = HubGroup.create_group(group_name)
    assign_group_to_user(group=hub_group, user=user)
    return hub_group


def create_hub_and_assign_to_group(group: HubGroup, hub_name: str = "Unnamed hub"):
    hub = Hub.create_hub(name=hub_name)
    assign_hub_to_group(hub=hub, group=group)
    return hub
