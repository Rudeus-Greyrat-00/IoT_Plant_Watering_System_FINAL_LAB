from .common import *
from db_classes.classes_si_db.user import Users
from db_classes.classes_si_db.hubgroups import HubGroups
from db_classes.classes_si_db.hubs import Hubs


def assign_group_to_user(group : HubGroups, user: Users):
    """
    Assign an HubGroup object to an user given his user id
    :param group:
    :param user:
    :return: nothing
    """
    raise NotImplemented()


def assign_hub_to_group(hub: Hubs, group: HubGroups):
    """
    Given a Hub object and a group object, assign said Hub to the group
    :param hub:
    :param group:
    :return: nothing
    """
    raise NotImplemented()


def delete_hub(hub: Hubs):
    """
    Used when a user is deleted, or he removes a hub from his account
    :return: nothing
    """

    raise NotImplemented()


def delete_group(group: HubGroups):
    """
    Used when a user is deleted, or he removes a group from his account
    :return: nothing
    """
    for hub in group.hubs:
        delete_hub(hub)
    raise NotImplemented()


def delete_user(user: Users):
    """
    Used when an user delete his account, his groups and hubs are then deleted as well
    :return: nothing
    """
    for group in user.groups: # this is pseudo code but perhaps it would work
        delete_group(group)
    # delete user from db
    raise NotImplemented()
