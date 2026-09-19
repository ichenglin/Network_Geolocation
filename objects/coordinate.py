from objects.serializable import Serializable, SerializableContent


class Coordinate(Serializable):
    def __init__(self, latitude: float, longitude: float):
        self.latitude  = latitude
        self.longitude = longitude

    @classmethod
    def __import__(cls, content: SerializableContent):
        return cls(
            content.get("latitude",  None),
            content.get("longitude", None)
        )

    def __export__(self) -> SerializableContent:
        return {
            "latitude":  self.latitude,
            "longitude": self.longitude
        }

    def __str__(self):
        return f"(lat={self.latitude}, lng={self.longitude})"

    def __repr__(self):
        return self.__str__()

class ProximateCoordinate(Coordinate):
    def __init__(self, latitude: float, longitude: float, accuracy: float):
        super().__init__(latitude, longitude)
        self.accuracy = accuracy

    @classmethod
    def __import__(cls, content: SerializableContent):
        return cls(
            content.get("latitude",  None),
            content.get("longitude", None),
            content.get("accuracy",  None)
        )

    def __export__(self) -> SerializableContent:
        return {
            "latitude":  self.latitude,
            "longitude": self.longitude,
            "accuracy":  self.accuracy
        }

    def __str__(self):
        return f"(lat={self.latitude}, lng={self.longitude}, accuracy={self.accuracy})"

    def __repr__(self):
        return self.__str__()
