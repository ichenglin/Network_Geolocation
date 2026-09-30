from itertools import product
from typing import Self, TypeVar

from objects.serializable import Serializable, SerializableContent

T            = TypeVar("T")
type Sets[T] = list[T]

class Combination(Serializable):
    def __init__(self, bands: (list[int] | None) = None, channels: (list[int] | None) = None, amount: (int | None) = None, amount_raise: bool = True):
        self.bands        = bands
        self.channels     = channels
        self.amount       = amount
        self.amount_raise = amount_raise

    @classmethod
    def from_sets(cls, bands: (Sets[list[int]] | None) = None, channels: (Sets[list[int]] | None) = None, amounts: (Sets[int] | None) = None, amount_raise: bool = True) -> list[Self]:
        combinations = list(product(
            bands    or [None],
            channels or [None],
            amounts  or [None]
        ))
        return [cls(bands=combination[0], channels=combination[1], amount=combination[2], amount_raise=amount_raise) for combination in combinations]

    @classmethod
    def __import__(cls, content: SerializableContent) -> Self:
        return cls(
            content.get("bands",        None),
            content.get("channels",     None),
            content.get("amount",       None),
            content.get("amount_raise", None)
        )

    def __export__(self) -> SerializableContent:
        return {
            "bands":        self.bands,
            "channels":     self.channels,
            "amount":       self.amount,
            "amount_raise": self.amount_raise
        }

    def __str__(self) -> str:
        return f"(bnd={self.bands}, chs={self.channels}, amt={self.amount})"

    def __repr__(self) -> str:
        return self.__str__()
