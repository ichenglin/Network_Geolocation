# Wifi Geolocation Test

## Setup

```bash
cp .env.example .env
```

| Variable     | Description                                     |
|--------------|-------------------------------------------------|
| GEO_API      | API key for the Google Maps geolocation service |
| WLS_DEV      | WiFi device name in /dev                        |
| LOC_LAT      | Latitude of the actual location                 |
| LOC_LNG      | Longitude of the actual location                |

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

> NOTE: The test script must be run with sudo privileges to force rescan of WiFi networks

## References

- [Google Maps Geolocation API](https://developers.google.com/maps/documentation/geolocation/overview)
