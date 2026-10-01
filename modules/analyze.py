import random
import time
from itertools import product

from modules import io, map, sample, wifi
from modules.sample import Sampler
from objects.combination import Combination, Sets
from objects.coordinate import Coordinate
from objects.count import Count
from objects.result import Result
from objects.station import Station

METADATA_PATH = "data"
METADATA_NAME = "locations"
STATIONS_PATH = "data/stations"
STATIONS_NAME = "stations"
ANALYSIS_PATH = "data"
ANALYSIS_NAME = "result"
COUNTERS_PATH = "data"
COUNTERS_NAME = "counts"

def collect_stations(location: str, clusters: int, delay: int) -> None:
    for cluster in range(1, (clusters + 1)):
        print(f"> Collecting Cluster #{cluster}...")
        stations = wifi.get_stations()
        io.export_objects(f"{STATIONS_PATH}/{location}/{STATIONS_NAME}_{cluster}.json", stations)
        print(f"  Completed Cluster #{cluster}")
        if (cluster < clusters):
            time.sleep(delay)

def analyze_stations(clusters: int, combinations: list[Combination], sampler: Sampler = random.sample, get_result: bool = False, get_count: bool = False) -> None:
    metadatas   = io.import_raw    (f"{METADATA_PATH}/{METADATA_NAME}.json")
    coordinates = io.import_objects(f"{METADATA_PATH}/{METADATA_NAME}.json", Coordinate)
    results     = []
    counts      = []
    for index, metadata in enumerate(metadatas):
        location   = metadata.get("location")
        coordinate = coordinates[index]
        print(f"> Analyzing Location {location}... ({index + 1}/{len(metadatas)})")
        outputs = _analyze_clusters(location, coordinate, clusters, combinations, sampler, get_result, get_count)
        results.extend(outputs[0])
        counts .append(outputs[1])
        print(f"  Completed Location {location}")
    io.export_objects(f"{ANALYSIS_PATH}/{ANALYSIS_NAME}.json", results)
    io.export_objects(f"{COUNTERS_PATH}/{COUNTERS_NAME}.json", counts)

def _analyze_clusters(location: str, actual: Coordinate, clusters: int, combinations: list[Combination], sampler: Sampler, get_result: bool, get_count: bool) -> tuple[list[Result], Count]:
    total = []
    count = Count(location)
    for cluster in range(1, (clusters + 1)):
        stations = io.import_objects(f"{STATIONS_PATH}/{location}/{STATIONS_NAME}_{cluster}.json", Station)
        if (get_result):
            results = _analyze_bands(actual, stations, combinations, sampler)
            for result in results:
                result.set_location(location)
                result.set_cluster(cluster)
            total.extend(results)
        if (get_count):
            count.extend(stations)
    return (total, count)

def _analyze_bands(actual: Coordinate, stations: list[Station], combinations: list[Combination], sampler: Sampler) -> list[Result]:
    results = []
    for combination in combinations:
        try:
            samples  = sample.sample_all  (stations, combination, sampler)
            location = wifi  .get_geo     (samples)
            distance = map   .get_distance(actual, location)
            results.append(Result("", combination, -1, distance, location.accuracy, True))
        except RuntimeError as error:
            print(f"  Error: {error}")
            results.append(Result("", combination, -1, 0, 0, False))
    return results

def get_bands() -> list[int]:
    return [metadata.get("band") for metadata in wifi.WIRELESS_BANDS]

def get_bands_sets() -> Sets[list[int]]:
    bands        = get_bands()
    products     = list(product([False, True], repeat=len(bands)))
    combinations = [dict(zip(bands, combination)) for combination in products][1:]
    return [[band for band, active in combination.items() if active] for combination in combinations]