import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db import run_query

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Housing Market Intelligence",
    page_icon="🏠",
    layout="wide"
)

# -------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------
st.sidebar.title("🏠 Housing Market Intelligence")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "📊 Market Overview",
        "🏙️ City Explorer",
        "📈 Price Trends",
        "🔥 Speculation Index",
        "🏠 Rent vs Buy"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Data sources: Zillow, U.S. Census, FRED")

# -------------------------------------------------------
# HELPER: GET CITY LIST FOR DROPDOWNS
# -------------------------------------------------------
@st.cache_data
def get_cities():
    df = run_query("SELECT city, state FROM cities ORDER BY city")
    return [f"{row['city']}" for _, row in df.iterrows()]

# -------------------------------------------------------
# PAGE 1: MARKET OVERVIEW
# -------------------------------------------------------
if page == "📊 Market Overview":
    st.title("📊 Market Overview")
    st.markdown("Rankings and affordability metrics across all U.S. metros.")

    # --- Top metrics row ---
    col1, col2, col3 = st.columns(3)

    total_cities = run_query("SELECT COUNT(*) as cnt FROM cities").iloc[0]['cnt']
    latest_date = run_query("SELECT MAX(date) as d FROM home_prices").iloc[0]['d']
    avg_ratio = run_query("""
        SELECT ROUND(AVG(hp.median_home_value / il.median_household_income), 2) as avg_ratio
        FROM home_prices hp
        JOIN cities c ON hp.city_id = c.city_id
        JOIN income_levels il ON c.city_id = il.city_id AND YEAR(hp.date) = il.year
        WHERE il.year = 2023
    """).iloc[0]['avg_ratio']

    col1.metric("Cities Tracked", f"{total_cities:,}")
    col2.metric("Latest Data", str(latest_date))
    col3.metric("Avg Price-to-Income (2023)", f"{avg_ratio}x")

    st.markdown("---")

    # --- Affordability rankings table ---
    st.subheader("🏆 Affordability Rankings — 2023")

    year_filter = st.selectbox("Select Year", [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015], index=0)

    rankings = run_query(f"""
        SELECT
            c.city,
            c.state,
            ROUND(AVG(hp.median_home_value), 0) AS avg_home_value,
            il.median_household_income,
            ROUND(AVG(hp.median_home_value) / il.median_household_income, 2) AS price_to_income_ratio
        FROM home_prices hp
        JOIN cities c ON hp.city_id = c.city_id
        JOIN income_levels il ON c.city_id = il.city_id AND YEAR(hp.date) = il.year
        WHERE il.year = {year_filter}
        GROUP BY c.city_id, c.city, c.state, il.median_household_income
        ORDER BY price_to_income_ratio DESC
        LIMIT 50
    """)

    rankings.columns = ["City", "State", "Avg Home Value", "Median Income", "Price-to-Income Ratio"]
    rankings["Avg Home Value"] = rankings["Avg Home Value"].apply(lambda x: f"${x:,.0f}")
    rankings["Median Income"] = rankings["Median Income"].apply(lambda x: f"${x:,.0f}")

    st.dataframe(rankings, use_container_width=True, hide_index=True)