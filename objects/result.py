from typing import Self

from objects.combination import Combination
from objects.serializable import Serializable, SerializableContent
from objects.station import Station


class Result(Serializable):
    def __init__(self, location: str, combination: Combination, cluster: int, distance: float, confidence: float, success: bool, stations: (list[Station] | None) = None):
        self.location    = location
        self.combination = combination
        self.cluster     = cluster
        self.stations    = stations
        self.distance    = distance
        self.confidence  = confidence
        self.success     = success

    def set_location(self, location: str) -> None:
        self.location = location

    def set_cluster(self, cluster: int) -> None:
        self.cluster = cluster

    @classmethod
    def __import__(cls, content: SerializableContent) -> Self:
        combination = content.get("combination", None)
        stations    = content.get("stations",    None)
        return cls(
            content.get("location",   None),
            (Combination.__import__(combination) if combination else None),
            content.get("cluster",    None),
            content.get("distance",   None),
            content.get("confidence", None),
            content.get("success",    None),
            ([Station.__import__(station) for station in stations] if stations else None)
        )

    def __export__(self) -> SerializableContent:
        return {
            "location":    self.location,
            "combination": self.combination.__export__(),
            "cluster":     self.cluster,
            "distance":    self.distance,
            "confidence":  self.confidence,
            "success":     self.success,
            "stations":    ([station.__export__() for station in self.stations] if self.stations else None)
        }

    def __str__(self) -> str:
        return f"(loc={self.location}, ftr={self.combination}, scs={self.success})"

    def __repr__(self) -> str:
        return self.__str__()
