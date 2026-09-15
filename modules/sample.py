import random

from objects.station import Station


def sample_all(stations: list[Station], bands: (list[int] | None) = None, channels: (list[int] | None) = None, amount: (int | None) = None, amount_raise: bool = True) -> list[Station]:
    if bands:
        stations = list(filter(lambda station: (station.band in bands), stations))
    if channels:
        stations = list(filter(lambda station: (station.channel in channels), stations))
    if amount:
        try:
            stations = random.sample(stations, amount)
        except ValueError:
            if amount_raise:
                raise ValueError(f"Not enough stations ({len(stations)}) to sample ({amount})")
    return stations