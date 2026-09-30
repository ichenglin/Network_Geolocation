from abc import ABC, abstractmethod
from typing import Self

type SerializableContent = dict[str, (int | float | str | bool)]

class Serializable(ABC):
    @classmethod
    @abstractmethod
    def __import__(cls, content: SerializableContent) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __export__(self) -> SerializableContent:
        raise NotImplementedError