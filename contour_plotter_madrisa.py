import geopandas as gpd
from matplotlib import pyplot as plt

contour = gpd.read_file(r"madrisa_contour\contours\contours.shx")
contour.to_crs(epsg=3395)
contour.plot(color = "k")
plt.show()
