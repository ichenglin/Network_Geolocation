from modules import map, sample, wifi


def main() -> None:
    stations = wifi.get_stations()
    samples  = sample.sample_all(stations, channels=wifi.get_channels([2, 5]), amount=10)
    location = wifi.get_geo(samples)
    distance = map.get_distance(map.get_actual(), location)
    print(f"{int(distance)} meter(s)")


if __name__ == "__main__":
    main()
