import os
import re
import subprocess
from itertools import chain

import dotenv
import requests

from objects.coordinate import ProximateCoordinate
from objects.station import Station

dotenv.load_dotenv()

WIRELESS_CMD    = f"iw dev {os.getenv("WLS_DEV")} scan"
WIRELESS_BANDS  = [
    {"base": 2412, "start": 1,  "end": 14},
    {"base": 5160, "start": 32, "end": 177},
]
WIRELESS_BSS  = r'^BSS ((?:[\da-f]{2}:){5}[\da-f]{2})'
WIRELESS_PROP = r'^\t+([\w ]+): ([^:]*)$'
GEO_URL = f"https://www.googleapis.com/geolocation/v1/geolocate?key={os.getenv("GEO_API")}"

def get_stations() -> list[dict]:
    try:
        result               = subprocess.check_output(WIRELESS_CMD.split(), text=True)
        stations: list[dict] = []
        for line in result.splitlines():
            # match BSS
            match_bss = re.match(WIRELESS_BSS, line)
            if match_bss:
                stations.append({"bss": match_bss.group(1)})
                continue
            # match property
            match_prop = re.match(WIRELESS_PROP, line)
            if match_prop:
                stations[-1][match_prop.group(1)] = match_prop.group(2)
        return [Station(
            bss    =station.get("bss"),
            ssid   =station.get("SSID", None),
            channel=get_channel(int(float(station.get("freq")))),
            signal =int(float(station.get("signal").split()[0]))
        ) for station in stations]
    except subprocess.CalledProcessError:
        print("ERROR: wifi scan returned non-zero")
        return []

def get_geo(stations: list[Station]) -> ProximateCoordinate:
    payload = {
        "considerIp":       False,
        "wifiAccessPoints": [{
            "macAddress":     station.bss,
            "signalStrength": station.signal,
            "channel":        station.channel
        } for station in stations]
    }
    result   = requests.post(GEO_URL, json=payload)
    response = result.json()
    error    = response.get("error", None)
    if error:
        raise RuntimeError(error.get("message", "Unknown"))
    return ProximateCoordinate(response["location"]["lat"], response["location"]["lng"], response["accuracy"])

def get_channel(frequency: int) -> int:
    for band in WIRELESS_BANDS:
        channel = (((frequency - band["base"]) // 5) + band["start"])
        if ((channel < band["start"]) or (channel > band["end"])):
            continue
        return channel
    return 0

def get_channels(band_ids: list[int]) -> list[int]:
    bands    = filter(lambda band: ((band["base"] // 1000) in band_ids), WIRELESS_BANDS)
    channels = [range(band["start"], (band["end"] + 1)) for band in bands]
    return list(chain.from_iterable(channels))
