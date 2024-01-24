from db_classes.classes_si_db.hubgroups import HubGroups
from db_classes.classes_si_db.hubs import Hubs
from db_classes.classes_si_db.user import Users
from .object_management_utilities import assign_group_to_user, assign_hub_to_group


def create_group_and_assign_to_user(user: Users, location, group_name: str = "Unnamed group"):
    hub_group = HubGroups.create_group(location=location, name=group_name)
    assign_group_to_user(group=hub_group, user=user)
    return hub_group


def create_hub_and_assign_to_group(group: HubGroups, desired_humidity, watering_frequency, hub_name: str = "Unnamed hub"):
    hub = Hubs.create_hub(name=hub_name, desired_humidity=desired_humidity, watering_frequency=watering_frequency)
    assign_hub_to_group(hub=hub, group=group)
    return hub
