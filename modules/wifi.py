import os
import re
import subprocess

import dotenv
import requests

from objects.coordinate import ProximateCoordinate
from objects.station import Station

dotenv.load_dotenv()

GEO_URL         = f"https://www.googleapis.com/geolocation/v1/geolocate?key={os.getenv("GEO_API")}"
MAC_BROADCAST   = "FF:FF:FF:FF:FF:FF"
MAC_RESERVED    = "00:00:5E"
WIRELESS_BSS    = r'^BSS ((?:[\da-f]{2}:){5}[\da-f]{2})'
WIRELESS_PROP   = r'^\t+([\w ]+): ([^:]*)$'
WIRELESS_NULL   = r'^(?:\\x00)+$'
WIRELESS_CMD    = f"iw dev {os.getenv("WLS_DEV")} scan"
WIRELESS_BANDS  = [
    {"band": 2, "base": 2412, "start": 1,  "end": 14},
    {"band": 5, "base": 5160, "start": 32, "end": 177},
    {"band": 6, "base": 5955, "start": 1,  "end": 233}
]

def get_stations() -> list[dict]:
    while True:
        try:
            result               = subprocess.check_output(WIRELESS_CMD.split(), text=True)
            stations: list[dict] = []
            for line in result.splitlines():
                # match BSS
                match_bss = re.match(WIRELESS_BSS, line)
                if match_bss:
                    stations.append({"bss": match_bss.group(1), "raw": [line]})
                    continue
                # match property
                match_prop = re.match(WIRELESS_PROP, line)
                if match_prop:
                    stations[-1][match_prop.group(1)] = match_prop.group(2)
                    stations[-1].get("raw").append(line)
            return [Station(
                bss    = station.get("bss"),
                ssid   = get_ssid(station.get("SSID", None)),
                band   = band,
                channel= channel,
                signal = int(float(station.get("signal").split()[0])),
                raw    = station.get("raw")
            ) for station       in stations
            for band, channel in [get_band(int(float(station.get("freq"))))]
            if (
                (station.get("bss")    .upper() != MAC_BROADCAST) and
                (station.get("bss")[:8].upper() != MAC_RESERVED)
            )]
        except subprocess.CalledProcessError as error:
            print(f"ERROR: {error.stderr}")

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

def get_ssid(ssid_nullable: (str | None)) -> (int | None):
    if (not ssid_nullable):
        return None
    null_matcher = re.match(WIRELESS_NULL, ssid_nullable)
    return (None if null_matcher else ssid_nullable)

def get_band(frequency: int) -> tuple[int, int]:
    for band in WIRELESS_BANDS:
        channel = (((frequency - band["base"]) // 5) + band["start"])
        if ((channel < band["start"]) or (channel > band["end"])):
            continue
        return (band["band"], channel)
    return (0, 0)
