from db_classes.classes_si_db.hubgroups import HubGroups
from db_classes.classes_si_db.hubs import Hubs
from db_classes.classes_si_db.user import Users


def assign_group_to_user(group : HubGroups, user: Users):
    """
    Assign an HubGroup object to a user given his user id
    :param group:
    :param user:
    :return: nothing
    """
    user.groups.append(group)
    user.save()


def assign_hub_to_group(hub: Hubs, group: HubGroups):
    """
    Given a Hub object and a group object, assign said Hub to the group
    :param hub:
    :param group:
    :return: nothing
    """
    group.hubs.append(hub)
    group.save()


def delete_hub(hub: Hubs):
    """
    Used when a user is deleted, or he removes a hub from his account
    :return: nothing
    """
    hub.delete()


def delete_group(group: HubGroups):
    """
    Used when a user is deleted, or he removes a group from his account
    :return: nothing
    """
    for hub in group.hubs:
        delete_hub(hub)
    group.delete()


def delete_user(user: Users):
    """
    Used when a user delete his account, his groups and hubs are then deleted as well
    :return: nothing
    """
    for group in user.groups:
        delete_group(group)
    user.delete()
