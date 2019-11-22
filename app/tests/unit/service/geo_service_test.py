from decimal import Decimal
import app.main.service.geo_service as unit
from geopy.distance import Distance


def test_distance_between_two_points():
    cord1 = [Decimal(75.3425), Decimal(-95.300)]
    cord2 = [Decimal(76.6543), Decimal(-95.3566)]
    expectedDistance = Distance(146.44140729201737)

    difference = expectedDistance.km  - unit.calculate_distance(cord1, cord2).km
    assert abs(difference) <= 0.00001


def test_point_in_run_map_zone():
    cord1 = [Decimal(75.3425), Decimal(-95.300)]
    cord2 = [Decimal(76.6543), Decimal(-95.3566)]
    cord3 = [Decimal(75.34254), Decimal(-95.3005)]
    assert not unit.is_point_in_zone(cord1, cord2)
    assert unit.is_point_in_zone(cord1, cord3)


def test_get_city_name():
    cord = [Decimal(44.946636), Decimal(-93.293241)]
    assert 'Minneapolis' == unit.get_city_name(cord)

    cord = [Decimal(41.565111), Decimal(-73.543925)]
    assert 'Quaker Hill' == unit.get_city_name(cord)
