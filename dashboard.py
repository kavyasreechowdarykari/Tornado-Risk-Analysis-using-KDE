import streamlit as st
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import io

# Page config
st.set_page_config(layout="wide")
st.title("USA Tornado Risk Assessment Dashboard")

# LOAD DATA 
@st.cache_data
def load_data():
    gdf = gpd.read_file(
        "/Users/kavyasreechowdary/Downloads/MS project/tornado_projected_2015_2025.geojson"
    )
    gdf["x"] = gdf.geometry.x
    gdf["y"] = gdf.geometry.y
    return gdf

gdf = load_data()

# Loading State BOUNDARIES
@st.cache_data
def load_states():
    states = gpd.read_file(
        "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    )
    states = states.to_crs(epsg=5070)
    return states

usa_states = load_states()

st.sidebar.header("Dashboard")
state = st.sidebar.selectbox(
    "Select State",
    sorted(gdf["State"].unique())
)
year_range = st.sidebar.slider(
    "Year Range",
    int(gdf["Year"].min()),
    int(gdf["Year"].max()),
    (2015, 2025)
)
kernel = st.sidebar.selectbox(
    "Kernel Type",
    ["gaussian", "tophat", "epanechnikov"]
)
bandwidth = st.sidebar.slider(
    "Bandwidth (meters)",
    5000, 50000, 20000
)
distance_miles = bandwidth / 1609
st.sidebar.write("Estimated Risk Radius:", round(distance_miles, 2), "miles")

grid_size = st.sidebar.slider(
    "Grid Resolution",
    50, 300, 100
)
if grid_size > 200:
    st.sidebar.warning("High grid resolution may slow down performance")

generate = st.sidebar.button("Generate Risk Map")

if generate:

    data = gdf.copy()
    data = data[data["State"] == state]
    data = data[
        (data["Year"] >= year_range[0]) &
        (data["Year"] <= year_range[1])
    ]

    if len(data) < 5:
        st.warning("Not enough data for this selection")
        st.stop()

    st.info(f"Using {len(data)} tornado records")

    coords = data[["x", "y"]].values

    kde = KernelDensity(
        bandwidth=bandwidth,
        kernel=kernel
    )
    kde.fit(coords)

    xmin, ymin, xmax, ymax = data.total_bounds

    xgrid = np.linspace(xmin, xmax, int(grid_size))
    ygrid = np.linspace(ymin, ymax, int(grid_size))
    xx, yy = np.meshgrid(xgrid, ygrid)

    grid_coords = np.vstack([xx.ravel(), yy.ravel()]).T

    log_density = kde.score_samples(grid_coords)
    density = np.exp(log_density).reshape(xx.shape)

    density = density - density.min()
    if density.max() != 0:
        density = density / density.max()

    density_norm = density * 100

    fig, ax = plt.subplots(figsize=(10, 7))
    heat = ax.imshow(
        density_norm,
        extent=[xmin, xmax, ymin, ymax],
        origin="lower",
        cmap="hot",
        alpha=0.9
    )


    selected_state_boundary = usa_states[usa_states["name"] == state]
    selected_state_boundary.boundary.plot(ax=ax, color="black", linewidth=2.2)

    ax.scatter(
        data["x"], data["y"],
        s=3,
        color="blue",
        alpha=0.3
    )

    plt.colorbar(heat, ax=ax, label="Risk (0–100)")

    ax.set_title(
        f"{state} Tornado Risk Map | Bandwidth: {bandwidth} m"
    )

    st.pyplot(fig)
    risk_value = round(density_norm.mean(), 2)

    st.subheader("Tornado Risk Value")
    st.metric("Risk", risk_value)

    if risk_value < 33:
        category = "Low Risk"
    elif risk_value < 66:
        category = "Moderate Risk"
    else:
        category = "High Risk"

    st.write("Risk Category:", category)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")

    st.download_button(
        label="Download Risk Map",
        data=buf.getvalue(),
        file_name=f"{state}_tornado_risk.png",
        mime="image/png"
    )