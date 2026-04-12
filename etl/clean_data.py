import pandas as pd
import os

# Paths to the raw and cleaned data

RAW_DIR = "data/raw"
CLEAN_DIR = "data/clean"

os.makedirs(CLEAN_DIR, exist_ok = True)

# Load the raw data

zhvi_raw = pd.read_csv(f"{RAW_DIR}/zhvi_metro.csv")
zori_raw = pd.read_csv(f"{RAW_DIR}/zori_metro.csv")

print("Raw ZHVI data shape:", zhvi_raw.shape)
print("Raw ZORI data shape:", zori_raw.shape)

# Drop Rows that are not Metro Areas, drop US national row

zhvi_raw = zhvi_raw[zhvi_raw["RegionType"] == "msa"]
zori_raw = zori_raw[zori_raw["RegionType"] == "msa"]

print("\nAfter filtering to metro only:")
print("ZHVI rows:", len(zhvi_raw))
print("ZORI rows:", len(zori_raw))

# Identify date columns, and melt from wide to long format

zhvi_date_cols = [c for c in zhvi_raw.columns if c[:4].isdigit()]
zori_date_cols = [c for c in zori_raw.columns if c[:4].isdigit()]

zhvi_long = zhvi_raw.melt(
    id_vars=["RegionID", "RegionName", "StateName"],
    value_vars=zhvi_date_cols,
    var_name="date",
    value_name="median_home_value"
)

zori_long = zori_raw.melt(
    id_vars=["RegionID", "RegionName", "StateName"],
    value_vars=zori_date_cols,
    var_name="date",
    value_name="median_rent"
)

print("\nAfter melting to long format:")
print("ZHVI rows:", len(zhvi_long))
print("ZORI rows:", len(zori_long))

# Cleaning up columns

# convert date columns to datetime
zhvi_long["date"] = pd.to_datetime(zhvi_long["date"])
zori_long["date"] = pd.to_datetime(zori_long["date"])   

# Round values to 2 decimal places for simplicity
zhvi_long["median_home_value"] = zhvi_long["median_home_value"].round(2)
zori_long["median_rent"] = zori_long["median_rent"].round(2)

# Standardize city name columns
zhvi_long = zhvi_long.rename(columns={"RegionName": "city" , "StateName": "state"})
zori_long = zori_long.rename(columns={"RegionName": "city" , "StateName": "state"})

# Align Date ranges (trim ZHVI down to 2015 onward to match ZORI)

zhvi_long = zhvi_long[zhvi_long["date"] >= "2015-01-01"]

print("\nAfter cleaning and aligning date ranges:")
print("ZHVI rows:", len(zhvi_long))
print("ZORI rows:", len(zori_long))

# drop rows with missing values
zhvi_before = len(zhvi_long)
zori_before = len(zori_long)

zhvi_long = zhvi_long.dropna(subset=["median_home_value"])
zori_long = zori_long.dropna(subset=["median_rent"])

print(f"\nZHVI rows dropped due to missing values: {zhvi_before - len(zhvi_long)}")
print(f"ZORI rows dropped due to missing values: {zori_before - len(zori_long)}")

# sort and saving cleaned data

zhvi_long = zhvi_long.sort_values(["city", "date"]).reset_index(drop = True)
zori_long = zori_long.sort_values(["city", "date"]).reset_index(drop = True)

zhvi_long.to_csv(f"{CLEAN_DIR}/zhvi_clean.csv", index = False)
zori_long.to_csv(f"{CLEAN_DIR}/zori_clean.csv", index = False)

print("\n Cleaned files and saved to data/cleaned/")
print("ZHVI final shape:", zhvi_long.shape)
print("ZORI final shape:", zori_long.shape)
print(zhvi_long.head(3).to_string())
print("\n Sample ZORI rows:")
print(zori_long.head(3).to_string())

# Census data cleaning

import glob

# find all data CSV files
census_dir = f"{RAW_DIR}/census"
census_files = glob.glob(f"{census_dir}/*-Data.csv")
print(f"\nFound {len(census_files)} Census data files")

census_frames = []

for filepath in census_files:
    # Extract the year from the filename (assuming format like "ACSST5Y2015.S1901-Data.csv")
    filename = os.path.basename(filepath)
    year = int(filename[8:11])

    # Read the CSV file and skip the second row 
    df = pd.read_csv(filepath, header = 0,  dtype = str)

    # keep only the columns we need, and rename them
    #  S1901_C01_012E = median household income estimate
    keep_cols = ["GEO_ID", "NAME", "S1901_C01_012E"]
    df = df[keep_cols]

    df = df.rename(columns={
        'GEO_ID': "geo_id",
        "NAME": "city",
        "S1901_C01_012E": "median_household_income"
    })

    # Add a year column
    df["year"] = year

    census_frames.append(df)

# Combine all years into a single DataFrame
census_data = pd.concat(census_frames, ignore_index = True)

print("\nCombined Census data shape:", census_data.shape)

# Clean up census data

census = census_data

# Strip " Metro Area" and " Metropolitan Statistical Area" from city names
census["city"] = census["city"].str.replace(" Metro Area", "", regex=False)
census["city"] = census["city"].str.replace(" Metropolitan Statistical Area", "", regex=False)

# Drop rows where income is missing or non-numeric
# Census uses '-', 'N', '**' etc. for suppressed/unavailable data
census = census[pd.to_numeric(census["median_household_income"], errors="coerce").notna()]
census["median_household_income"] = census["median_household_income"].astype(float).round(2)

# Drop the GEO_ID column as it's not needed for our analysis and is just a unique identifier
census = census.drop(columns=["geo_id"])

# Sort by city and year for easier analysis later
census = census.sort_values(["city", "year"]).reset_index(drop=True)

print(f"Census rows after cleaning: {len(census)}")
print("\nSample Census rows:")
print(census.head(5).to_string())

# Save cleaned census data to one clean CSV
census.to_csv(f"{CLEAN_DIR}/census_income_clean.csv", index=False)
print("\n Census income saved to data/cleaned/census_income_clean.csv")
