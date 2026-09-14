from modules import io, map, report, sample, wifi


def report_distance() -> None:
    stations = wifi.get_stations()
    actual   = map.get_actual()
    samples  = sample.sample_all(stations, channels=wifi.get_channels([2, 5]), amount=None)
    location = wifi.get_geo(samples)
    distance = map.get_distance(actual, location)
    report.report_border()
    report.report_samples(samples, key="channel", reverse=False)
    report.report_border()
    report.report_distance(actual, location, distance)
    report.report_border()

def save_stations() -> None:
    stations = wifi.get_stations()
    io.export_objects("data/out.json", stations)

if __name__ == "__main__":
    report_distance()
    #save_stations()
