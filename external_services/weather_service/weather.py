
# ----- INTERFACES ----- #




# ----- API ----- #


# ------ TEST ------ #
from ..location_service.location import search_address, search_coordinates

if __name__ == "__main__":

    print(search_address("Via Marche 32 Assemini"), search_coordinates("Via Marche 32 Assemini"))
