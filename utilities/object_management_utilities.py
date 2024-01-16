from .common import *
from db_classes.classes_si_db.user import User
from db_classes.classes_si_db.hubgroup import HubGroup
from db_classes.classes_si_db.hub import Hub


def assign_group_to_user(group : HubGroup, user: User):
    """
    Assign an HubGroup object to an user given his user id
    :param group:
    :param user:
    :return: nothing
    """
    raise NotImplemented()


def assign_hub_to_group(hub: Hub, group: HubGroup):
    """
    Given a Hub object and a group object, assign said Hub to the group
    :param hub:
    :param group:
    :return: nothing
    """
    raise NotImplemented()


def delete_hub(hub: Hub):
    """
    Used when a user is deleted, or he removes a hub from his account
    :return: nothing
    """

    raise NotImplemented()


def delete_group(group: HubGroup):
    """
    Used when a user is deleted, or he removes a group from his account
    :return: nothing
    """
    for hub in group.hubs:
        delete_hub(hub)
    raise NotImplemented()


def delete_user(user: User):
    """
    Used when an user delete his account, his groups and hubs are then deleted as well
    :return: nothing
    """
    for group in user.groups: # this is pseudo code but perhaps it would work
        delete_group(group)
    # delete user from db
    raise NotImplemented()
