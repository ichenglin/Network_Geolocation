import time

from modules import io, map, report, sample, wifi


def report_distance() -> None:
    stations = wifi.get_stations()
    actual   = map.get_actual()
    samples  = sample.sample_all(stations, bands=[2, 5], amount=None)
    location = wifi.get_geo(samples)
    distance = map.get_distance(actual, location)
    report.report_border()
    report.report_samples(samples, key="channel", reverse=False)
    report.report_border()
    report.report_distance(actual, location, distance)
    report.report_border()

def save_stations(location: str, clusters: int, delay: int) -> None:
    for cluster in range(1, (clusters + 1)):
        print(f"> Collecting Cluster #{cluster}...")
        stations = wifi.get_stations()
        io.export_objects(f"data/{location}/data_{cluster}.json", stations)
        print(f"  Completed Cluster #{cluster}")
        if (cluster < clusters):
            time.sleep(delay)

if __name__ == "__main__":
    report_distance()
    #save_stations("dev", 1, 3)
