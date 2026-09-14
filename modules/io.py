import json
from pathlib import Path
from typing import TypeVar

from objects.serializable import Serializable

T = TypeVar("T", bound=Serializable)


def import_objects(file: str, container: type[T]) -> list[T]:
    with open(file, "r") as file_stream:
        datas = json.load(file_stream)
    return [container.__import__(data) for data in datas]
    
def export_objects(file: str, datas: list[T]) -> None:
    Path(file).parent.mkdir(parents=True, exist_ok=True)
    with open(file, "w") as file_stream:
        json.dump([data.__export__() for data in datas], file_stream, indent="\t")

def import_object(file: str, container: type[T]) -> T:
    return import_objects(file, container)[0]

def export_object(file: str, content: T) -> None:
    export_objects(file, [content])