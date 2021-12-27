import pandas as pd
import numpy as np
import os
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from matplotlib import pyplot as plt
import geopandas as gpd

folder = r"routes"
routes = np.zeros(np.size(os.listdir(folder)),dtype=object)
for i,filename in enumerate(os.listdir(folder)):

    df = pd.read_excel(f"{folder}/{filename}")

    df = df.drop(labels="index", axis=1)
    df = df.dropna(axis=1)

    df["position"] = df["posistion"]
    df = df.drop(labels="posistion", axis=1)

    df["altitude"] = np.array([float(x.strip("m")) for x in df["height"].values])

    positionarray = np.array([x.replace("N", "")
                              .replace("°", "")
                              .replace("'","")
                              .replace("E", "")
                              .split() for x in df["position"].values])
    df["latitude"] = np.array([float(x[0]) + 1/60 * float(x[1]) for x in positionarray]) # - 0.315
    df["longitude"] = np.array([float(x[2]) + 1/60 * float(x[3]) for x in positionarray])
    routes[i] = df

plt.figure(figsize=(12,12))
terrain = cimgt.Stamen('terrain-background')
mp = plt.axes(projection=terrain.crs)

# exclude madrisa
routes = np.hstack((routes[:2], routes[3:]))

right_corner = [10.349620, 47.223494]
left_corner = [10.629468, 47.113881]

for route in routes:
    mp.plot(route["longitude"], route["latitude"], c = "royalblue", ls = "--", transform=ccrs.PlateCarree())

mp.set_extent([right_corner[0] * 0.998, left_corner[0] * 1.002,
               left_corner[1] * 0.9997, right_corner[1] * 1.0003])

mp.add_image(terrain, 12)
plt.show()

