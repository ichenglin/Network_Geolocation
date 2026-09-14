import json
from typing import TypeVar

from objects.serializable import Serializable

T = TypeVar("T", bound=Serializable)

def import_object(file: str, container: type[T]) -> T:
    with open(file, "r") as file_stream:
        data = json.load(file_stream)
    return container.__import__(data)

def export_object(file: str, content: T) -> None:
    with open(file, "w") as file_stream:
        json.dump(content.__export__(), file_stream)
