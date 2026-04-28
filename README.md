# Housing Market Intelligence Platform

> A SQL-powered analytics platform for evaluating U.S. housing affordability, price trends, and speculation signals across major metro areas.

---

## Overview

Housing data in the U.S. is fragmented across dozens of disconnected sources, making it difficult to form a clear, data-driven picture of any given market. This project aggregates publicly available housing and economic data into a structured MySQL database and exposes it through a library of analytical SQL queries and an interactive Streamlit dashboard.

The platform is built to answer questions like:

- Which cities are becoming unaffordable, and how fast?
- Where is price growth significantly outpacing income growth — a classic signal of speculation?
- Is it currently better to rent or buy in a given metro area?
- Which markets show the earliest signs of overheating?

---

## Project Status

🟡 **In Development — Phase 4 ~ Working on visualizing data and queries through a streamlit dashboard**

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Data acquisition & cleaning | ✅ Complete |
| 2 | MySQL database build & ETL | ✅ Complete |
| 3 | SQL query development | ✅ Complete |
| 4 | Streamlit dashboard | 🔄 In progress |

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
├── queries/          # Analytical SQL query library (10+ queries)
├── etl/              # Python scripts for data cleaning and DB loading
├── dashboard/        # Streamlit app
├── docs/             # PRD and project documentation
│
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
cities           → Master reference table (city_id, name, state, region)
home_prices      → Monthly median home values (FK: city_id)
rent_prices      → Monthly median rent (FK: city_id)
income_levels    → Annual median household income (FK: city_id)
interest_rates   → National monthly 30-yr mortgage rates (no city FK)
affordability_metrics → Derived metrics computed from above tables
```

Full DDL scripts are located in `/database`.

---

## Key Metrics

| Metric | Formula |
|--------|---------|
| Price-to-Income Ratio | Median Home Price / Median Household Income |
| Rent-to-Income Ratio | Annual Rent / Median Household Income |
| Estimated Monthly Mortgage | Based on 20% down, 30-yr fixed at current FRED rate |
| Rent vs. Buy Ratio | Monthly Rent / Estimated Monthly Mortgage |
| Price Growth (YoY) | (Current Price − Prior Year Price) / Prior Year Price |
| Speculation Index | Price Growth YoY − Income Growth YoY |

---

## SQL Query Library

Queries are organized in `/queries` and cover eight analytical categories:

1. City lookup & filtering
2. Affordability ratios (price-to-income, rent-to-income)
3. Price growth analysis (YoY, rolling averages)
4. Income growth vs. price growth (speculation detection)
5. Rent vs. buy comparison
6. Rent burden analysis (30% threshold flagging)
7. Time-series trending (window functions)
8. Market rankings & summary views

---

## Dashboard Views (Streamlit)

The Streamlit app (in `/dashboard`) includes five interactive views:

- **City Explorer** — select one or more cities and compare all key metrics side by side
- **Affordability Rankings** — sortable table of cities ranked by price-to-income or rent burden
- **Price Growth Trends** — time-series line chart of home values for selected cities
- **Speculation Dashboard** — chart comparing price growth vs. income growth by city and year
- **Rent vs. Buy Calculator** — input a city and year to see estimated mortgage vs. rent

---

## Getting Started

### Prerequisites
- Python 3.9+
- MySQL 8.0+
- MySQL Workbench (recommended for query development)

### Installation

```bash
# Clone the repository
git clone https://github.com/CarsonPociask/housing-market-intelligence.git
cd housing-market-intelligence

# Install Python dependencies
pip install -r requirements.txt

# Set up the database
# Run the DDL scripts in /database against your local MySQL instance

# Load the data
python etl/load_data.py

# Launch the dashboard
streamlit run dashboard/app.py
```

> Full setup instructions will be added as each phase is completed.

---

## Documentation

The full Product Requirements Document (PRD) is available in [`/docs`](./docs).

---

## Author

**Carson Pociask**
- GitHub: [@CarsonPociask](https://github.com/CarsonPociask)
- LinkedIn: [carson-pociask](https://www.linkedin.com/in/carson-pociask-28a597325/)
