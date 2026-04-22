import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity

# Load Projected Tornado Data
gdf = gpd.read_file(
    "/Users/kavyasreechowdary/Downloads/MS project/tornado_projected_2015_2025.geojson"
)

print("Total Tornado Records:", len(gdf))

def generate_kde(state_name=None, bandwidth=20000):
    """
    state_name = None → Entire USA
    state_name = "Texas" → Only Texas
    bandwidth in meters (default 20km)
    """
    if state_name is None:
        data = gdf
        print("Generating KDE for Entire USA")
    else:
        data = gdf[gdf["State"] == state_name]
        print(f"Generating KDE for {state_name}")

    if len(data) < 5:
        print("Not enough tornado data")
        return None, None, None

    print("Tornado count:", len(data))

    coords = np.vstack([data.geometry.x, data.geometry.y]).T
    kde = KernelDensity(bandwidth=bandwidth, kernel="gaussian")
    kde.fit(coords)
    xmin, ymin, xmax, ymax = data.total_bounds
    xgrid = np.linspace(xmin, xmax, 200)
    ygrid = np.linspace(ymin, ymax, 200)
    xx, yy = np.meshgrid(xgrid, ygrid)

    grid_coords = np.vstack([xx.ravel(), yy.ravel()]).T
    log_density = kde.score_samples(grid_coords)
    density = np.exp(log_density)

    return xx, yy, density.reshape(xx.shape)

xx, yy, density = generate_kde(None)

if density is not None:
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, density, levels=50)
    plt.colorbar(label="Tornado Density")
    plt.title("Tornado Density (2015–2025)")
    plt.xlabel("X (meters)")
    plt.ylabel("Y (meters)")
    plt.show()
else:
    print("KDE could not be generated due to insufficient data.")