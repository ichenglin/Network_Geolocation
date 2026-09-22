# Wifi Geolocation Test

## Setup

The `iw` package is used to scan for WiFi networks.
If it is not already installed, install it with the following command:
```bash
sudo apt install iw
```

Copy and populate the `.env` file with your configuration:
```bash
cp .env.example .env
```

| Variable     | Description                                     |                             |
|--------------|-------------------------------------------------|-----------------------------|
| GEO_API      | API key for the Google Maps geolocation service | Required                    |
| WLS_DEV      | WiFi device name in `/dev`                      | Required                    |
| LOC_ACT      | Actual location in `latitude, longitude`        | Used by `report_distance()` |

> [!TIP]
> Even if `report_distance()` is not used, the `LOC_ACT` variable should still be set to a valid coordinate (e.g. `0, 0`).

## Run Test

Setup python virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the test script:

```bash
sudo .venv/bin/python test.py
```

> [!IMPORTANT]
> The test script must be run with sudo privileges to force rescan of WiFi networks

## Example Output

```console
(.venv) user@device:~/geolocation$ sudo .venv/bin/python test.py
[sudo: authenticate] Password:

=========================================================================
1  | It hertz when IP | 2 GHz | Channel 2   | -62 dBm | 11:11:11:11:11:11
2  | Lord of the Ping | 2 GHz | Channel 3   | -58 dBm | 22:22:22:22:22:22
3  |                  | 2 GHz | Channel 5   | -68 dBm | 33:33:33:33:33:33
4  | WuTangLAN        | 2 GHz | Channel 8   | -71 dBm | 44:44:44:44:44:44
5  | Drop It Like It' | 2 GHz | Channel 10  | -50 dBm | 55:55:55:55:55:55
6  | I believe Wi-Can | 5 GHz | Channel 149 | -63 dBm | 66:66:66:66:66:66
7  | SamsungSmartToil | 5 GHz | Channel 153 | -80 dBm | 77:77:77:77:77:77
8  |                  | 5 GHz | Channel 153 | -64 dBm | 88:88:88:88:88:88
9  |                  | 6 GHz | Channel 85  | -82 dBm | 99:99:99:99:99:99
10 | Router I Hardly  | 6 GHz | Channel 213 | -80 dBm | aa:aa:aa:aa:aa:aa
=========================================================================
Guess:       37.255806, -115.80549
Actual:      37.255808, -115.80562
Uncertainty: 16.223    meter(s)
Distance:    11.520633 meter(s)
=========================================================================
```

## References

- [Google Maps Geolocation API](https://developers.google.com/maps/documentation/geolocation/overview)
- [List of WLAN channels](https://en.wikipedia.org/wiki/List_of_WLAN_channels)
