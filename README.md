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

## References

- [Google Maps Geolocation API](https://developers.google.com/maps/documentation/geolocation/overview)
