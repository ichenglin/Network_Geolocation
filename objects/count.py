from collections import Counter

from objects.serializable import Serializable, SerializableContent


class Count(Serializable):
    def __init__(self, location: str, counts: dict[int, int] | None = None):
        self.location = location
        self.counter  = Counter(counts or {})

    def get_counter(self) -> Counter[int]:
        return self.counter

    def set_counter(self, counter: Counter[int]) -> None:
        self.counter = counter

    @classmethod
    def __import__(cls, content: SerializableContent):
        return cls(
            content.get("location", None),
            content.get("counts",   None)
        )

    def __export__(self) -> SerializableContent:
        return {
            "location": self.location,
            "counts":   dict(self.counter)
        }

    def __str__(self) -> str:
        return f"(loc={self.location})"

    def __repr__(self) -> str:
        return self.__str__()
