import pandas as pd
import mysql.connector
import os

# Database connection 

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "236404CPpuffin*", #replace with your actual password and actual mysql user
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

home_prices_data = []
for _, row in zhvi.iterrows():
    city_id = city_lookup.get((row["city"], row["state"]))
    if city_id is None:
        continue
    home_prices_data.append((
        city_id,
        row["date"],
        row["median_home_value"]
    ))


print(f"\nHome prices rows to insert: {len(home_prices_data)}")

# Insert home prices data in batches as there are many rows

batch_size = 1000
for i in range(0, len(home_prices_data), batch_size):
    batch = home_prices_data[i:i + batch_size]
    cursor.executemany("""
        INSERT IGNORE INTO home_prices (city_id, date, median_home_value)
        VALUES (%s, %s, %s)
    """, batch)
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM home_prices")
count = cursor.fetchone()[0]
print(f"Home prices loaded: {count} rows in database")

# Load the rental_prices table

rent_prices_data = []

for _, row in zori.iterrows():
    city_id = city_lookup.get((row["city"], row["state"]))
    if city_id is None:
        continue
    rent_prices_data.append((
        city_id,
        row["date"],
        row["median_rent"]
    ))

print(f"\nRent prices rows to insert: {len(rent_prices_data)}")

for i in range(0, len(rent_prices_data), batch_size):
    batch = rent_prices_data[i:i + batch_size]
    cursor.executemany("""
        INSERT IGNORE INTO rent_prices (city_id, date, median_rent)
        VALUES (%s, %s, %s)
    """, batch)
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM rent_prices")
count = cursor.fetchone()[0]
print(f"Rent prices loaded: {count} rows in database")

# Load interest rates data

interest_rates_data = []

for _, row in fred.iterrows():
    interest_rates_data.append((
        row["date"],
        row["mortgage_rate_30yr"]
    ))

print(f"\nInterest rate rows to insert: {len(interest_rates_data)}")

for i in range(0, len(interest_rates_data), batch_size):
    batch = interest_rates_data[i:i + batch_size]
    cursor.executemany("""
        INSERT IGNORE INTO interest_rates (date, mortgage_rate_30yr)
        VALUES (%s, %s)
    """, batch)
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM interest_rates")
count = cursor.fetchone()[0]
print(f"Interest rates loaded: {count} rows in database")

# Load income data 
income_data = []
skipped = 0
for _, row in census.iterrows():
    # Census city names don't include state, so we need to find the city_id by matching just on city name
    city_name = row["city"]
    # We have to extract state from city name in census data, which is in format "Abilene, TX" — state is the last 2 chars after ","
    if "," in city_name:
        state = city_name.split(",")[-1].strip()
    else: 
        skipped += 1
        continue
    city_id = city_lookup.get((city_name, state))
    if city_id is None:
        skipped += 1
        continue
    income_data.append((
        city_id,
        int(row["year"]),
        row["median_household_income"]
    ))

print(f"\nIncome rows to insert: {len(income_data)}")
print(f"Rows skipped: {skipped}")

# DEBUG - find unmatched census cities
unmatched = []
for _, row in census.iterrows():
    city_name = row["city"]
    if ", " in city_name:
        state = city_name.split(", ")[-1].strip()
        city_id = city_lookup.get((city_name, state))
        if city_id is None:
            unmatched.append(city_name)

unmatched_unique = sorted(set(unmatched))
print(f"\nSample unmatched Census cities (first 20):")
for c in unmatched_unique[:20]:
    print(f"  {c}")
    
for i in range(0, len(income_data), batch_size):
    batch = income_data[i:i + batch_size]
    cursor.executemany("""
        INSERT IGNORE INTO income_levels (city_id, year, median_household_income)
        VALUES (%s, %s, %s)
    """, batch)
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM income_levels")
count = cursor.fetchone()[0]
print(f"Income levels loaded: {count} rows in database")

cursor.close()
conn.close()
