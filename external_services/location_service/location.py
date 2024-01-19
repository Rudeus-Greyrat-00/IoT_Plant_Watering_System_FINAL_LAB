"""
Interface file to abstract location_service services
"""
from geopy import location

# ----- LOCATION SERVICES ----- #

from ._bing import geolocator


def search_location(locality: str) -> location:
    """
    :param locality:
    :return: a geolocator location type
    """
    return geolocator.geocode(locality)


def search_address(locality: str) -> str:
    """
    :param locality:
    :return: an actual address
    """
    return geolocator.geocode(locality).address


def search_coordinates(locality: str):
    """
    :param locality:
    :return: an actual address
    """
    actual_locality = geolocator.geocode(locality)
    return actual_locality.latitude, actual_locality.longitude
