# Wifi Geolocation Test

## Setup

```bash
cp .env.example .env
```

| Variable     | Description                                     |
|--------------|-------------------------------------------------|
| GEO_API      | API key for the Google Maps geolocation service |
| WLS_DEV      | WiFi device name in `/dev`                      |
| LOC_ACT      | Actual location in `latitude, longitude`        |

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

=================================================================
1  | It hertz when IP | Channel 2   | -62 dBm | 11:11:11:11:11:11
2  | Lord of the Ping | Channel 3   | -58 dBm | 22:22:22:22:22:22
3  |                  | Channel 5   | -68 dBm | 33:33:33:33:33:33
4  | WuTangLAN        | Channel 8   | -71 dBm | 44:44:44:44:44:44
5  | Drop It Like It' | Channel 10  | -50 dBm | 55:55:55:55:55:55
6  | I believe Wi-Can | Channel 149 | -63 dBm | 66:66:66:66:66:66
7  | SamsungSmartToil | Channel 153 | -80 dBm | 77:77:77:77:77:77
8  |                  | Channel 153 | -64 dBm | 88:88:88:88:88:88
9  |                  | Channel 157 | -82 dBm | 99:99:99:99:99:99
10 | Router I Hardly  | Channel 157 | -80 dBm | aa:aa:aa:aa:aa:aa
=================================================================
Guess:    37.255806, -115.80549
Actual:   37.255808, -115.80562
Distance: 11 meter(s)
=================================================================
```

## References

- [Google Maps Geolocation API](https://developers.google.com/maps/documentation/geolocation/overview)
