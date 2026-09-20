import time
from itertools import product

from modules import io, map, sample, wifi
from objects.coordinate import Coordinate
from objects.result import Result
from objects.station import Station

METADATA_PATH = "data"
METADATA_NAME = "locations"
STATIONS_PATH = "data/stations"
STATIONS_NAME = "stations"
ANALYSIS_PATH = "data"
ANALYSIS_NAME = "result"

def collect_stations(location: str, clusters: int, delay: int) -> None:
    for cluster in range(1, (clusters + 1)):
        print(f"> Collecting Cluster #{cluster}...")
        stations = wifi.get_stations()
        io.export_objects(f"{STATIONS_PATH}/{location}/{STATIONS_NAME}_{cluster}.json", stations)
        print(f"  Completed Cluster #{cluster}")
        if (cluster < clusters):
            time.sleep(delay)

def analyze_stations(clusters: int) -> None:
    metadatas   = io.import_raw    (f"{METADATA_PATH}/{METADATA_NAME}.json")
    coordinates = io.import_objects(f"{METADATA_PATH}/{METADATA_NAME}.json", Coordinate)
    results     = []
    for index, metadata in enumerate(metadatas):
        location   = metadata.get("location")
        coordinate = coordinates[index]
        print(f"> Analyzing Location {location}... ({index + 1}/{len(metadata)})")
        results.extend(_analyze_clusters(location, coordinate, clusters))
        print(f"  Completed Location {location}")
    io.export_objects(f"{ANALYSIS_PATH}/{ANALYSIS_NAME}.json", results)

def _analyze_clusters(location: str, actual: Coordinate, clusters: int) -> list[Result]:
    results = []
    for cluster in range(1, (clusters + 1)):
        stations = io.import_objects(f"{STATIONS_PATH}/{location}/{STATIONS_NAME}_{cluster}.json", Station)
        results  = _analyze_bands(actual, stations)
        for result in results:
            result.set_location(location)
            result.set_cluster(cluster)
        results.extend(results)
    return results
    

def _analyze_bands(actual: Coordinate, stations: list[Station]) -> list[Result]:
    combinations = _get_combinations()
    results      = []
    for combination in combinations:
        try:
            bands    = [band for band, active in combination.items() if active]
            samples  = sample.sample_all  (stations, bands=bands)
            location = wifi  .get_geo     (samples)
            distance = map   .get_distance(actual, location)
            results.append(Result("", combination, -1, distance, True))
        except RuntimeError:
            results.append(Result("", combination, -1, 0, False))
    return results


def _get_combinations() -> list[dict[int, bool]]:
    bands        = [metadata.get("band") for metadata in wifi.WIRELESS_BANDS]
    combinations = list(product([False, True], repeat=len(bands)))
    return [dict(zip(bands, combination)) for combination in combinations][1:]