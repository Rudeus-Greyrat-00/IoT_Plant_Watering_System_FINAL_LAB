# ----- INTERFACES ----- #


# ----- API ----- #


# ------ TEST ------ #
from external_services.location_service.location import search_address, search_coordinates

if __name__ == "__main__":
    print(search_address("Assemini"), search_coordinates("Assemini"))
