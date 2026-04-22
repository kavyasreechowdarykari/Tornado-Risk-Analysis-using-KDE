import pandas as pd

# Load your dataset
input_file = "/Users/kavyasreechowdary/Downloads/MS project/Tornado data (2015-2025).csv"
df = pd.read_csv(input_file)

print("Original Shape:", df.shape)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df = df.dropna(subset=["Magnitude"])

valid_ef = ["EF0", "EF1", "EF2", "EF3", "EF4", "EF5"]
df = df[df["Magnitude"].isin(valid_ef)]
df["EF_Scale"] = df["Magnitude"].str.replace("EF", "").astype(int)
df["State"] = df["State"].str.title()
df = df.dropna(subset=["Latitude", "Longitude"])

df = df[
    (df["Latitude"].between(20, 50)) &
    (df["Longitude"].between(-130, -60))
]

print("Cleaned Shape:", df.shape)
output_file = "/Users/kavyasreechowdary/Downloads/MS project/Tornado cleaned 2015_2025.csv"
df.to_csv(output_file, index=False)

print("Total Tornado Records:", len(df))