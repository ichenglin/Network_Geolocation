import os
import re
import subprocess

import dotenv
import requests

dotenv.load_dotenv()

WIRELESS_CMD    = f"iw dev {os.getenv("WLS_DEV")} scan"
WIRELESS_BANDS  = [
    {"base": 2412, "start": 1,  "end": 14},
    {"base": 5160, "start": 32, "end": 177},
]
WIRELESS_BSS  = r'^BSS ((?:[\da-f]{2}:){5}[\da-f]{2})'
WIRELESS_PROP = r'^\t+([\w ]+): ([^:]*)$'
GEO_URL = f"https://www.googleapis.com/geolocation/v1/geolocate?key={os.getenv("GEO_API")}"

def get_channel(frequency: int) -> int:
    for band in WIRELESS_BANDS:
        channel = (((frequency - band["base"]) // 5) + band["start"])
        if ((channel < band["start"]) or (channel > band["end"])):
            continue
        return channel
    return 0

def get_wifi() -> list[dict]:
    try:
        result   = subprocess.check_output(WIRELESS_CMD.split(), text=True)
        stations = []
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
        return stations
    except subprocess.CalledProcessError:
        print("ERROR: wifi scan returned non-zero")
        return []

def get_geo(stations: list[dict]) -> dict:
    payload = {
        "considerIp":       False,
        "wifiAccessPoints": [{
            "macAddress":     station["bss"],
            "signalStrength": int(float(station["signal"].split()[0])),
            "channel":        get_channel(int(float(station["freq"])))
        } for station in stations]
    }
    result = requests.post(GEO_URL, json=payload)
    result.raise_for_status()
    return result.json()
