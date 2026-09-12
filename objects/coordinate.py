class Coordinate:
    def __init__(self, latitude: float, longitude: float):
        self.latitude  = latitude
        self.longitude = longitude

    def __str__(self):
        return f"(lat={self.latitude}, lng={self.longitude})"

    def __repr__(self):
        return self.__str__()

class ProximateCoordinate(Coordinate):
    def __init__(self, latitude: float, longitude: float, accuracy: float):
        super().__init__(latitude, longitude)
        self.accuracy = accuracy

    def __str__(self):
        return f"(lat={self.latitude}, lng={self.longitude}, accuracy={self.accuracy})"

    def __repr__(self):
        return self.__str__()
