import json
import os
from pathlib import Path
from typing import TypeVar

from objects.serializable import Serializable

T = TypeVar("T", bound=Serializable)

ID_USER  = os.environ.get("SUDO_UID")
ID_GROUP = os.environ.get("SUDO_GID")

def import_objects(file: str, container: type[T]) -> list[T]:
    with open(file, "r") as file_stream:
        datas = json.load(file_stream)
    return [container.__import__(data) for data in datas]
    
def export_objects(file: str, datas: list[T]) -> None:
    Path(file).parent.mkdir(parents=True, exist_ok=True)
    with open(file, "w") as file_stream:
        json.dump([data.__export__() for data in datas], file_stream, indent="\t")
    _fix_folder(str(Path(file).parent))

def import_object(file: str, container: type[T]) -> T:
    return import_objects(file, container)[0]

def export_object(file: str, content: T) -> None:
    export_objects(file, [content])

def _fix_file(path: str) -> None:
    if (ID_USER is None) or (ID_GROUP is None):
        return
    os.chown(path, int(ID_USER), int(ID_GROUP), follow_symlinks=False)

def _fix_folder(path: str) -> None:
    _fix_file(path)
    for root, directories, files in os.walk(path):
        for name in (directories + files):
            _fix_file(os.path.join(root, name))
