# Geographical Analysis of Tornado Risk Using Kernel Density Estimation

This project presents a geospatial analysis of tornado risk using historical data and Kernel Density Estimation (KDE). It transforms discrete tornado events into a continuous risk surface and provides an interactive dashboard for visualization and exploration.


## Project Overview

Tornadoes are highly unpredictable and destructive natural events. Traditional approaches visualize tornado occurrences as discrete points, which do not effectively represent how risk is distributed across a region.

This project addresses that limitation by:
- Applying Kernel Density Estimation (KDE) to model spatial risk
- Converting tornado data into a geospatial format
- Generating continuous tornado risk maps
- Building an interactive dashboard using Streamlit


## Dataset

- Source: NOAA (National Oceanic and Atmospheric Administration)
- Time Period: 2015 – 2025
- Records: 16,462 (cleaned to 14,824)
- Attributes:
  - Date
  - Latitude & Longitude
  - State
  - Tornado Intensity (EF Scale)


##  Methodology

1. **Data Cleaning**
   - Removed missing and invalid values
   - Converted date to datetime format
   - Filtered valid EF-scale tornadoes (EF0–EF5)
   - Standardized state names and coordinates

2. **GeoDataFrame Conversion**
   - Converted latitude & longitude into spatial points
   - Set CRS to WGS84 (EPSG:4326)
   - Reprojected to EPSG:5070 (meters) for accurate distance calculations

3. **Kernel Density Estimation (KDE)**
   - Extracted spatial coordinates (x, y)
   - Applied KDE using Gaussian kernel
   - Controlled smoothing using bandwidth
   - Generated grid for continuous risk estimation
   - Normalized output to 0–100 risk scale

4. **Visualization**
   - Generated heatmaps representing tornado risk
   - Displayed tornado points and state boundaries


##  Interactive Dashboard (Streamlit)

The dashboard allows users to:
- Select state
- Filter by year range
- Choose kernel type (Gaussian, Tophat, Epanechnikov)
- Adjust bandwidth (risk radius)
- Modify grid resolution (map detail)
- Generate real-time tornado risk maps
- Download generated maps


