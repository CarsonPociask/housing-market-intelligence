# Housing Market Intelligence Platform

> A SQL-powered analytics platform for evaluating U.S. housing affordability, price trends, and speculation signals across major metro areas.

---

## Overview

Housing data in the U.S. is fragmented across dozens of disconnected sources, making it difficult to form a clear, data-driven picture of any given market. This project aggregates publicly available housing and economic data into a structured MySQL database and exposes it through a library of analytical SQL queries and an interactive Streamlit dashboard.

The platform is built to answer questions like:

- Which cities are becoming unaffordable, and how fast?
- Where is price growth significantly outpacing income growth — a classic signal of speculation?
- Is it currently better to rent or buy in a given metro area?
- How has a city's affordability changed over the past decade?
- Which markets show the earliest signs of overheating/strutural stress?

---

## Project Status
Complete - All four phases delivered.

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Data acquisition & cleaning | ✅ Complete |
| 2 | MySQL database build & ETL | ✅ Complete |
| 3 | SQL query development | ✅ Complete |
| 4 | Streamlit dashboard | ✅ Complete |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Database | MySQL 8.0+ |
| Data Processing | Python (pandas, PyMySQL) |
| Query Development | MySQL Workbench / VS Code |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Version Control | Git + GitHub |

---

## Repository Structure

```
housing-market-intelligence/
│
├── data/
│   ├── raw/          # Original downloaded CSVs (Zillow, Census, FRED)
│   └── clean/      # Python-processed CSVs ready for DB load
│
├── database/         # DDL scripts — CREATE TABLE definitions
│   ├── 01_create_cities.sql
│   ├── 02_create_home_prices.sql
│   ├── 03_create_rent_prices.sql
│   ├── 04_create_income_levels.sql
│   ├── 05_create_interest_rates.sql
│   └── 06_create_affordability_metrics.sql
├── queries/          # Analytical SQL query library
│   ├── 01_city_home_prices.sql
│   ├── 02_most_recent_prices.sql
│   ├── 03_price_to_income_ratio.sql
│   ├── 04_rent_to_income_ratio.sql
│   ├── 05_price_growth_yoy.sql
│   ├── 06_speculation_index.sql
│   ├── 07_rent_vs_buy.sql
│   ├── 08_rolling_12mo_avg.sql
│   ├── 09_affordability_over_time.sql
│   └── 10_market_summary_ranking.sql
│
├── etl/              # Python scripts for data cleaning and DB loading
│   ├── clean_data.py     # Cleans and normalizes all four raw datasets
│   └── load_data.py      # Loads cleaned CSVs into MySQL
├── dashboard/        # Streamlit app
│   ├── app.py            # Streamlit application
│   └── db.py             # Database connection helper
├── docs/             # PRD and project documentation
│
├── .env                
├── .gitignore
└── README.md
```

---

## Data Sources

| Source | Dataset | Use |
|--------|---------|-----|
| [Zillow Research](https://www.zillow.com/research/data/) | ZHVI (Home Value Index) | Median home prices by city/month |
| [Zillow Research](https://www.zillow.com/research/data/) | ZORI (Observed Rent Index) | Median rent by city/month |
| [U.S. Census / ACS](https://data.census.gov/) | Median Household Income | Annual income by metro area |
| [FRED](https://fred.stlouisfed.org/) | 30-Year Fixed Mortgage Rate | National monthly mortgage rates |

> Raw data files are excluded from this repository via `.gitignore` due to file size. See the links above to download the source datasets.

---

## Database Schema

The platform uses a normalized six-table MySQL schema:

```
cities                → Master reference table (city_id, city, state)
home_prices           → Monthly median home values by city (FK: city_id)
rent_prices           → Monthly median rent by city (FK: city_id)
income_levels         → Annual median household income by city (FK: city_id)
interest_rates        → National weekly 30-yr fixed mortgage rate (no city FK)
affordability_metrics → Derived metrics table (populated from queries)
```
Scale: 907 metropolitan areas · 119,255 home price records · 49,231 rent records · 3,740 income records · 588 mortgage rate observations

Full DDL scripts are located in `/database`.

---

## Key Metrics

| Metric | Formula | Threshold |
|--------|---------|-----------|
| Price-to-Income Ratio | Median Home Price / Median Household Income | > 5.0x = unaffordable |
| Rent-to-Income Ratio | Annual Rent / Median Household Income × 100 | > 30% = rent burdened |
| Est. Monthly Mortgage | Amortization formula, 20% down, 30-yr fixed at FRED rate | — |
| Rent-to-Mortgage Ratio | Monthly Rent / Est. Monthly Mortgage | > 1.0 = rent favored |
| Price Growth YoY | (Current − Prior Year) / Prior Year × 100 | — |
| Speculation Index | Price Growth YoY % − Income Growth YoY % | > 15pp = high pressure |
| Market Stress Score | 0.5×PTI + 0.3×(RTI/10) + 0.2×Price Growth | > 7 = high stress |

---

## SQL Query Library

Queries are organized in `/queries` and cover ten analytical categories:

| Query | Category | Key Concepts |
|-------|----------|--------------|
| `01_city_home_prices.sql` | City lookup | `JOIN`, `WHERE`, `ORDER BY` |
| `02_most_recent_prices.sql` | Point-in-time | Subquery, `MAX()` |
| `03_price_to_income_ratio.sql` | Affordability | Three-table join, `AVG()`, computed column |
| `04_rent_to_income_ratio.sql` | Rent burden | `CASE WHEN`, threshold flagging |
| `05_price_growth_yoy.sql` | Growth analysis | `LAG()` window function, `PARTITION BY` |
| `06_speculation_index.sql` | Speculation | Dual window function subqueries joined |
| `07_rent_vs_buy.sql` | Rent vs. buy | Amortization formula, `POWER()`, four-table join |
| `08_rolling_12mo_avg.sql` | Trend smoothing | `AVG() OVER`, `ROWS BETWEEN` |
| `09_affordability_over_time.sql` | Longitudinal | `LAG()` on derived ratios, multi-year trend |
| `10_market_summary_ranking.sql` | Composite ranking | CTEs (`WITH`), weighted composite scoring |
---

## Dashboard Views (Streamlit)

The Streamlit app (in `/dashboard`) includes si interactive views:

| Page | Description |
|------|-------------|
| **Market Overview** | National affordability rankings, composite market stress scatter, year-selectable filters |
| **City Explorer** | Detailed per-city profile: price-to-income ratio trend, home value vs. income, monthly price history with rolling average |
| **Price Trends** | Multi-city comparison of monthly prices, 12-month rolling averages, and year-over-year growth rates |
| **Speculation Index** | Rankings and scatter analysis of price growth vs. income growth divergence by city and year |
| **Rent vs. Buy** | Rent-to-mortgage ratio distribution and per-city rent vs. estimated mortgage over time |
| **Data Explorer** | Filterable, downloadable access to all underlying datasets: home prices, rent, income, mortgage rates, and affordability summary |

---

## Getting Started

### Prerequisites
- Python 3.9+
- MySQL 8.0+
- MySQL Workbench (recommended)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/CarsonPociask/housing-market-intelligence.git
cd housing-market-intelligence

# 2. Install Python dependencies
pip install pandas pymysql sqlalchemy streamlit plotly python-dotenv cryptography

# 3. Download source datasets (see Data Sources section above)
#    Place files in data/raw/ as:
#      zhvi_metro.csv
#      zori_metro.csv
#      census/ (folder containing ACS S1901 annual CSVs)
#      fred_mortgage.csv

# 4. Run the cleaning pipeline
python etl/clean_data.py

# 5. Create the database in MySQL Workbench
#    Run all scripts in database/ in order (01 through 06)

# 6. Configure environment variables
#    Create a .env file in the repo root:
#      DB_HOST=localhost
#      DB_USER=root
#      DB_PASSWORD=your_password
#      DB_NAME=housing_intelligence

# 7. Load data into MySQL
python etl/load_data.py

# 8. Launch the dashboard
cd dashboard
streamlit run app.py
```
## Some Selected Findings
 
A few findings that emerged from the data:
 
- **Kahului, HI** holds the highest price-to-income ratio in the dataset at 10.64x in 2023 — meaning the median home costs over a decade of the median household's gross income. Likely due to out of state tourists leading to inreased demand than what would be suistained by the true local population.
- **Florida dominates rent burden rankings** — 9 of the top 20 most rent-burdened metros in 2023 are in Florida, led by Miami at 41.98% rent-to-income. Likely due to simmilar reasons as hawaii, many people like to vacation in florida leading to a signifigant rental market. 
- **Idaho cities drove the largest speculation signals in 2021** — Boise City led with a 28.06pp divergence between price growth (35.9%) and income growth (7.86%), consistent with the pandemic-era migration shock.
- **Austin, TX** experienced one of the sharpest pandemic run-ups and corrections in the dataset — peaking at ~$563k in mid-2022 before falling back to ~$424k by early 2026.
- **Chicago** showed remarkable affordability stability across the entire 2015–2024 period, with a price-to-income ratio holding between 3.2x and 3.5x throughout.
- **At 6.8% mortgage rates in 2023**, virtually all high-cost coastal markets are buy-unfavorable on a monthly cash-flow basis — San Jose's rent-to-mortgage ratio of 0.42 means rent costs less than half the estimated mortgage.

```
## Author

**Carson Pociask**
- GitHub: [@CarsonPociask](https://github.com/CarsonPociask)
- LinkedIn: [carson-pociask](https://www.linkedin.com/in/carson-pociask-28a597325/)
