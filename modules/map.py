import os
from math import atan2, cos, radians, sin, sqrt

import dotenv

from objects.coordinate import Coordinate

EARTH_RADIUS = 6378137 # meters

dotenv.load_dotenv()

def get_actual() -> Coordinate:
    return Coordinate(
        latitude =float(os.environ["LOC_LAT"]),
        longitude=float(os.environ["LOC_LNG"])
    )

# distance (meters) between two points using haversine formula
def get_distance(coordinate_1: Coordinate, coordinate_2: Coordinate) -> float:
    radian_1, radian_2 = map(
        _get_radians, [coordinate_1, coordinate_2]
    )
    diff_latitude  = radian_2[0] - radian_1[0]
    diff_longitude = radian_2[1] - radian_1[1]
    haversine = (
          sin(diff_latitude / 2)**2
        + cos(radian_1[0])
        * cos(radian_2[0])
        * sin(diff_longitude / 2)**2
    )
    angular_distance = 2 * atan2(sqrt(haversine), sqrt(1 - haversine))
    return EARTH_RADIUS * angular_distance

def _get_radians(coordinate: Coordinate) -> tuple[float, float]:
    return tuple(map(radians, [coordinate.latitude, coordinate.longitude]))