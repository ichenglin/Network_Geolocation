import random

from objects.combination import Combination
from objects.station import Station


def sample_all(stations: list[Station], combination: Combination) -> list[Station]:
    if combination.bands:
        stations = list(filter(lambda station: (station.band in combination.bands), stations))
    if combination.channels:
        stations = list(filter(lambda station: (station.channel in combination.channels), stations))
    if combination.amount:
        try:
            stations = random.sample(stations, combination.amount)
        except ValueError:
            if combination.amount_raise:
                raise ValueError(f"Not enough stations ({len(stations)}) to sample ({combination.amount})")
    return stations