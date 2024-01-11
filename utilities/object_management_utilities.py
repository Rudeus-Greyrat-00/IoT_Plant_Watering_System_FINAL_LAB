from common import *
from db_classes.classes_si_db.user import User
from db_classes.classes_si_db.hubgroup import HubGroup
from db_classes.classes_si_db.hub import Hub


def assign_group_to_user(group : HubGroup, user_id: str):
    """
    Assign an HubGroup object to an user given his user id
    :param group:
    :param user_id:
    :return:
    """
    raise NotImplemented()


def assign_hub_to_group(hub: Hub, group: HubGroup):
    """
    Given a Hub object and a group object, assign said Hub to the group
    :param hub:
    :param group:
    :return:
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
    raise NotImplemented()


def delete_user(user: User):
    """
    Used when an user delete his account, his groups and hubs are then deleted as well
    :return: nothing
    """
