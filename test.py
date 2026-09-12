import wifi

def main() -> None:
    stations = wifi.get_wifi()
    location = wifi.get_geo(stations)
    print(location)
    print(f"For Google Maps: {location["location"]["lat"]}, {location["location"]["lng"]}")

if __name__ == "__main__":
    main()