from objects.serializable import Serializable, SerializableContent


class Result(Serializable):
    def __init__(self, location: str, bands: dict[int, bool], cluster: int, distance: float, confidence: float, success: bool):
        self.location   = location
        self.bands      = bands
        self.cluster    = cluster
        self.distance   = distance
        self.confidence = confidence
        self.success    = success

    def set_location(self, location: str) -> None:
        self.location = location

    def set_cluster(self, cluster: int) -> None:
        self.cluster = cluster

    @classmethod
    def __import__(cls, content: SerializableContent):
        return cls(
            content.get("location",   None),
            content.get("bands",      None),
            content.get("cluster",    None),
            content.get("distance",   None),
            content.get("confidence", None),
            content.get("success",    None)
        )

    def __export__(self) -> SerializableContent:
        return {
            "location":   self.location,
            "bands":      self.bands,
            "cluster":    self.cluster,
            "distance":   self.distance,
            "confidence": self.confidence,
            "success":    self.success
        }

    def __str__(self) -> str:
        return f"(loc={self.location}, bnd={self.bands}, scs={self.success})"

    def __repr__(self) -> str:
        return self.__str__()
