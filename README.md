# Wifi Geolocation Test

| Distance by Location and Band | CDF                       |
|:-----------------------------:|:-------------------------:|
| ![](https://raw.githubusercontent.com/ichenglin/Network_Geolocation/refs/heads/main/images/distance_by_location_wifi_bands.png) | ![](https://raw.githubusercontent.com/ichenglin/Network_Geolocation/refs/heads/main/images/cdf_localization_distance_by_wifi_band.png) |

| Station Counts by Location | Channel Usage by Location          |
|:--------------------------:|:----------------------------------:|
| ![](https://raw.githubusercontent.com/ichenglin/Network_Geolocation/refs/heads/main/images/station_counts_by_location.png) | ![](https://raw.githubusercontent.com/ichenglin/Network_Geolocation/refs/heads/main/images/channel_usage_by_location_2ghz.png) |

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

## Report Distance

The test script uses `report_distance()` by default to evaluate the accuracy of the geolocation service by measuring the difference between its prediction and the known position. No files are created or modified when this function is used.
```python
# test.py

if __name__ == "__main__":
    report_distance()
    #analyze.collect_stations("location_1", 8, 10)
    #analyze.analyze_stations(8, get_total=True, get_count=True)
```

The output of the test script will look similar to the following:
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

## Analyze Stations

The `collect_stations(location, clusters, delay)` function can be used to collect WiFi station data for a given location. The `clusters` parameter specifies the number of scans to perform, and the `delay` parameter specifies the delay in seconds between scans. It saves the collected stations under the `data/stations/<location>` directory.
```python
# test.py

if __name__ == "__main__":
    #report_distance()
    analyze.collect_stations("location_1", 8, 10)
    #analyze.analyze_stations(8, get_total=True, get_count=True)
```

However, the `collect_stations()` function only collects the station data and does not record the grond truth location. Those locations must be recorded manually in the `data/locations.json` file, with `location` exactly matching the location parameter used in `collect_stations()`. The format of the file is as follows:
```json
[
    {
        "location": "location_1",
        "latitude": 37.255808,
        "longitude": -115.80562
    },
    {
        "location": "location_2",
        "latitude": 37.255806,
        "longitude": -115.80549
    },
    ...
]
```

The `analyze_stations(clusters, get_total, get_count)` function can then be used to analyze the collected data. The `clusters` parameter specifies the number of scans to analyze, the `get_total` (optional) parameter specifies whether to perform geolocation on the data, and the `get_count` (optional) parameter specifies whether to count the bands and channels of the stations. It saves the analysis results in `data/result.json` and `data/counts.json` respectively.
```python
# test.py

if __name__ == "__main__":
    #report_distance()
    #analyze.collect_stations("location_1", 8, 10)
    analyze.analyze_stations(8, get_total=True, get_count=True)
```

The output of the analysis will look similar to the following:
<details>
<summary>data/result.json</summary>

```json
[
    {
        "location": "location_1",
        "bands": {
            "2": false,
            "5": true,
            "6": false
        },
        "cluster": 1,
        "distance": 14.184323674122245,
        "confidence": 18.526,
        "success": true
    },
    ...
]
```
</details>

<details>
<summary>data/counts.json</summary>

```json
[
    {
		"location": "location_1",
		"bands": {
			"2": 13,
			"5": 8,
			"6": 4
		},
		"channels": {
			"2": {
				"11": 4,
				"6": 6,
				"1": 1,
				"8": 1,
				"5": 1
			},
			"5": {
				"64": 2,
				"48": 2,
				"108": 4
			},
			"6": {
				"85": 1,
				"165": 1,
				"21": 1,
				"181": 1
			}
		}
	},
    ...
]
```
</details>

## References

- [Google Maps Geolocation API](https://developers.google.com/maps/documentation/geolocation/overview)
- [List of WLAN channels](https://en.wikipedia.org/wiki/List_of_WLAN_channels)
