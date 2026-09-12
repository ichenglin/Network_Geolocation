from modules import map, sample, wifi

CHANNEL_2 = list(range(1,  14))
CHANNEL_5 = list(range(32, 177))

def main() -> None:
    stations = wifi.get_stations()
    samples  = sample.sample_all(stations, channels=(CHANNEL_2 + CHANNEL_5), amount=10)
    location = wifi.get_geo(samples)
    distance = map.get_distance(map.get_actual(), location)
    print(f"{int(distance)} meter(s)")


if __name__ == "__main__":
    main()
