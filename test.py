from modules import map, wifi


def main() -> None:
    stations = wifi.get_stations()
    location = wifi.get_geo(stations)
    distance = map.get_distance(map.get_actual(), location)
    print(location)
    print(f"~{int(distance)}m")

if __name__ == "__main__":
    main()
