from collections import Counter, defaultdict

from objects.serializable import Serializable, SerializableContent
from objects.station import Station


class Count(Serializable):
    def __init__(self, location: str, stations: (list[Station] | None) = None):
        self.location = location
        self.stations = Count.__to_named(stations or [])
        self.__refresh()

    def extend(self, stations: list[Station]) -> None:
        self.stations |= Count.__to_named(stations)
        self.__refresh()

    def __refresh(self) -> None:
        self.bands    = Counter(station.band for _, station in self.stations.items())
        self.channels = defaultdict(Counter)
        for station in self.stations.values():
            self.channels[station.band][station.channel] += 1

    @classmethod
    def __to_named(cls, stations: list[Station]) -> dict[str, Station]:
        return {station.bss: station for station in stations}

    @classmethod
    def __import__(cls, content: SerializableContent):
        # no import needed
        raise NotImplementedError

    def __export__(self) -> SerializableContent:
        return {
            "location": self.location,
            "bands":    dict(self.bands),
            "channels": {band: dict(channels) for band, channels in self.channels.items()}
        }

    def __str__(self) -> str:
        return f"(loc={self.location})"

    def __repr__(self) -> str:
        return self.__str__()
