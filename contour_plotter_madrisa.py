import geopandas as gpd
from matplotlib import pyplot as plt

contour = gpd.read_file(r"madrisa_contour/madrisa_contours.shp")
contour = contour[contour.geometry != None]
contour.to_crs(epsg=3395)
contour.plot(color = "k")
plt.show()
