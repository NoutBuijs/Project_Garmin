import pandas as pd
import numpy as np
import os
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from matplotlib import pyplot as plt
import geopandas as gpd

contour = gpd.read_file(r"madrisa_contour\contours\contours.shx")

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
route = 2

mp.set_extent([np.min(routes[route]["longitude"]) * 0.998, np.max(routes[route]["longitude"]) * 1.002,
              np.min(routes[route]["latitude"]) * 0.9997, np.max(routes[route]["latitude"]) * 1.0003])
mp.add_geometries(contour.geometry, crs=ccrs.PlateCarree(), facecolor='none', edgecolor='black')
mp.plot(routes[route]["longitude"], routes[route]["latitude"], c="darkred", ls = "--", transform=ccrs.Geodetic())
mp.add_image(terrain, 13, zorder=0)

plt.show()

