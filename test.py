from modules import analyze, map, report, sample, wifi


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

if __name__ == "__main__":
    report_distance()
    #analyze.analyze_stations(8, get_count=True)
