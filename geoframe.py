import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load cleaned dataset
df = pd.read_csv(
    "/Users/kavyasreechowdary/Downloads/MS project/Tornado cleaned 2015_2025.csv"
)

geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

gdf.set_crs(epsg=4326, inplace=True)
print("Original CRS:", gdf.crs)

gdf_projected = gdf.to_crs(epsg=5070)
print("Projected CRS:", gdf_projected.crs)

gdf_projected.to_file(
    "/Users/kavyasreechowdary/Downloads/MS project/tornado_projected_2015_2025.geojson",
    driver="GeoJSON"
)
gdf_projected.drop(columns="geometry").to_csv(
    "/Users/kavyasreechowdary/Downloads/MS project/tornado_projected_2015_2025.csv",
    index=False
)

print("Total records:", len(gdf_projected))