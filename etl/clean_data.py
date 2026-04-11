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

