from abc import ABC, abstractmethod

type SerializableContent = dict[str, (int | str | bool)]

class Serializable(ABC):
    @classmethod
    @abstractmethod
    def __import__(cls, content: SerializableContent):
        raise NotImplementedError

    @abstractmethod
    def __export__(self) -> SerializableContent:
        raise NotImplementedError