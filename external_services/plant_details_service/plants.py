"""
Interface file to abstract weather service services
"""
from _perenual import get_species as gs
from _perenual import get_species_details as gsd

# ----- INTERFACES ----- #


class PlantState:
    def __init__(self, common_name, scientific_name, description, watering, depth_water_requirement,
                 volume_water_requirement, watering_general_benchmark, sunlight, soil, growth_rate, default_image):
        self.common_name = common_name
        self.scientific_name = scientific_name
        self.description = description
        self.watering = watering
        self.depth_water_requirement = depth_water_requirement
        self.volume_water_requirement = volume_water_requirement
        self.watering_general_benchmark = watering_general_benchmark
        self.sunlight = sunlight
        self.soil = soil
        self.growth_rate = growth_rate
        self.default_image = default_image

    def __str__(self):
        pass


def get_species(species_name):
    species_dict = gs(species_name)
    return species_dict


def get_id_from_species_name(species_name):
    species_id = gs(species_name)['data'][0]['id']
    return species_id


def get_species_details(species_name) -> PlantState:
    idx = get_id_from_species_name(species_name)
    species_dict = gsd(idx)
    return PlantState(common_name=species_dict['common_name'], scientific_name=species_dict['scientific_name'],
                      description=species_dict['description'], watering=species_dict['watering'],
                      depth_water_requirement=species_dict['depth_water_requirement'],
                      volume_water_requirement=species_dict['volume_water_requirement'],
                      watering_general_benchmark=species_dict['watering_general_benchmark'],
                      sunlight=species_dict['sunlight'], soil=species_dict['soil'],
                      growth_rate=species_dict['growth_rate'], default_image=species_dict['default_image'])


if __name__ == '__main__':
    x = get_species_details('European Silver Fir')
    print(x.scientific_name)
