from geopy.distance import distance
from geopy.geocoders import Nominatim
MAP_ZONE_RADIUS = 50


def calculate_distance(cord1, cord2):
    return distance(cord1, cord2)


def is_point_in_zone(point, mapCenter):
    return distance(point, mapCenter) < MAP_ZONE_RADIUS


def get_city_name(cord):
    geolocator = Nominatim(user_agent="Strava Picture Genorator")
    address = geolocator.reverse(cord).raw['address']

    possibleDesignators = ['city', 'town', 'hamlet', 'village']
    cityName = ''
    for designator in possibleDesignators:
        cityName = address.get(designator, '')
        if not cityName == '':
            return cityName

    #if we can find a designator then just give a generic name
    return "Run Map"
