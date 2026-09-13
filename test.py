from modules import map, report, sample, wifi


def main() -> None:
    stations = wifi.get_stations()
    actual   = map.get_actual()
    samples  = sample.sample_all(stations, channels=wifi.get_channels([2, 5]), amount=10)
    location = wifi.get_geo(samples)
    distance = map.get_distance(actual, location)
    report.report_border()
    report.report_samples(samples)
    report.report_border()
    report.report_distance(actual, location, distance)
    report.report_border()

if __name__ == "__main__":
    main()
