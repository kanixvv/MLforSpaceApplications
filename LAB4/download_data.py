"""Download the Sentinel-2 cloudless (EOX, 2020) scenes used in LAB4.

Source: https://s2maps.eu  -  "Sentinel-2 cloudless 2020 by EOX IT Services GmbH"
(contains modified Copernicus Sentinel data 2020), licence CC BY-NC-SA 4.0.

Every scene is requested at about 10 m per pixel and its size is a multiple of
200 px, so it can be cut into 200 x 200 px patches (2 km x 2 km) without a remainder.
"""
import math
import pathlib
import urllib.request

WMS = "https://tiles.maps.eox.at/wms"
LAYER = "s2cloudless-2020"
OUT = pathlib.Path(__file__).parent / "data"
PATCH = 200          # patch side in pixels
M_PER_PX = 10.0

# name: (centre_lon, centre_lat, patches_across, patches_down)
SCENES = {
    # training scenes
    "urban_warszawa":    (21.010, 52.230, 6, 5),
    "urban_lodz":        (19.460, 51.765, 5, 4),
    "urban_wroclaw":     (17.030, 51.108, 5, 4),
    "urban_poznan":      (16.920, 52.405, 5, 4),
    "urban_katowice":    (18.980, 50.275, 6, 4),
    "forest_bialowieza": (23.800, 52.740, 6, 5),
    "forest_notecka":    (16.150, 52.730, 6, 4),
    "forest_dolnoslaskie": (15.300, 51.420, 6, 4),
    "forest_tucholskie": (17.900, 53.800, 5, 4),
    # test scenes (different places, never used for training)
    "urban_krakow":      (19.960, 50.065, 5, 4),
    "urban_gdansk":      (18.610, 54.370, 4, 4),
    "forest_niepolomice": (20.330, 50.045, 5, 3),
    "forest_kampinos":   (20.600, 52.320, 6, 3),
    "forest_augustowska": (23.250, 53.870, 5, 4),
}

def fetch(name, lon, lat, nx, ny):
    width, height = nx * PATCH, ny * PATCH
    dlon = width * M_PER_PX / (111_320 * math.cos(math.radians(lat)))
    dlat = height * M_PER_PX / 110_570
    bbox = (lon - dlon / 2, lat - dlat / 2, lon + dlon / 2, lat + dlat / 2)
    url = (f"{WMS}?service=WMS&version=1.1.1&request=GetMap&layers={LAYER}&styles="
           f"&srs=EPSG:4326&bbox={bbox[0]:.5f},{bbox[1]:.5f},{bbox[2]:.5f},{bbox[3]:.5f}"
           f"&width={width}&height={height}&format=image/jpeg")
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{name}.jpg"
    req = urllib.request.Request(url, headers={"User-Agent": "python-urllib"})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())
    print(f"{name}: {width}x{height} px -> {path}")

if __name__ == "__main__":
    for name, args in SCENES.items():
        fetch(name, *args)
