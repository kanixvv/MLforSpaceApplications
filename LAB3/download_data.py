"""Download the Sentinel-2 cloudless (EOX, 2020) crops used in LAB3.

Source: https://s2maps.eu  -  "Sentinel-2 cloudless 2020 by EOX IT Services GmbH"
(contains modified Copernicus Sentinel data 2020), licence CC BY-NC-SA 4.0.
"""
import math
import pathlib
import urllib.request

WMS = "https://tiles.maps.eox.at/wms"
LAYER = "s2cloudless-2020"
OUT = pathlib.Path(__file__).parent / "data"

# name: (min_lon, min_lat, max_lon, max_lat)
SCENES = {
    "forest_train": (19.775, 50.180, 19.865, 50.235),   # Ojcow National Park (near kracow)
    "urban_train":  (19.930, 50.040, 20.010, 50.085),   # central Krakow (east of the test scene)
    "test_scene":   (19.790, 50.020, 19.930, 50.090),   # Las Wolski / Bielany / western Krakow
}

def fetch(name, bbox, m_per_px=10.0):
    lon0, lat0, lon1, lat1 = bbox
    lat_mid = math.radians((lat0 + lat1) / 2)
    width = round((lon1 - lon0) * 111_320 * math.cos(lat_mid) / m_per_px)
    height = round((lat1 - lat0) * 110_570 / m_per_px)
    url = (f"{WMS}?service=WMS&version=1.1.1&request=GetMap&layers={LAYER}&styles="
           f"&srs=EPSG:4326&bbox={lon0},{lat0},{lon1},{lat1}"
           f"&width={width}&height={height}&format=image/jpeg")
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{name}.jpg"
    req = urllib.request.Request(url, headers={"User-Agent": "python-urllib"})
    with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
        f.write(r.read())
    print(f"{name}: {width}x{height} px -> {path}")

if __name__ == "__main__":
    for name, bbox in SCENES.items():
        fetch(name, bbox)
