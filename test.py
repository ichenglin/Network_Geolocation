from modules import wifi


def main() -> None:
    stations = wifi.get_stations()
    location = wifi.get_geo(stations)
    print(location)

if __name__ == "__main__":
    main()