import pandas as pd
import mysql.connector
import os

# Database connection 

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Passoword here", #replace with your actual password and actual mysql user
    database = "housing_intelligence"
)

cursor = conn.cursor()

# Load the clean data from the cleaned CSV files

CLEAN_DIR = "data/clean"

zhvi = pd.read_csv(f"{CLEAN_DIR}/zhvi_clean.csv")
zori = pd.read_csv(f"{CLEAN_DIR}/zori_clean.csv")
census = pd.read_csv(f"{CLEAN_DIR}/census_income_clean.csv")
fred = pd.read_csv(f"{CLEAN_DIR}/fred_mortgage_clean.csv")

print(f"ZHVI rows: {len(zhvi)}")
print(f"ZORI rows: {len(zori)}")
print(f"Census rows: {len(census)}")
print(f"FRED rows: {len(fred)}")

# load the cities table

# Get unique city/state combinations from both Zillow files combined
zhvi_cities = zhvi[["city", "state"]].drop_duplicates()
zori_cities = zori[["city", "state"]].drop_duplicates()
all_cities = pd.concat([zhvi_cities, zori_cities]).drop_duplicates().sort_values("city").reset_index(drop=True)

print(f"\nUnique cities to insert: {len(all_cities)}")

cities_inserted = 0

for _, row in all_cities.iterrows():
    try:
        cursor.execute("""
            INSERT IGNORE INTO cities (city, state)
            VALUES (%s, %s)
        """, (row["city"], row["state"]))
        cities_inserted += 1
    except Exception as e:
        print(f"Error inserting city {row['city']}: {e}")

conn.commit()
print(f"Cities loaded: {cities_inserted} rows inserted")


# Build city_id lookup dictionary 

cursor.execute("SELECT city_id, city, state FROM cities")
city_lookup = {(row[1], row[2]): row[0] for row in cursor.fetchall()}
print(f"City lookup built: {len(city_lookup)} entries")

# Load the home_prices table 


