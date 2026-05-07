import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from db import run_query

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="U.S. Housing Market Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------
# GLOBAL STYLES
# -------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300;1,8..60,400&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, .stApp {
        background-color: #FAF8F5 !important;
        font-family: 'Source Serif 4', Georgia, serif;
        color: #2C2C2C;
    }

    /* Hide sidebar entirely */
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }

    /* Remove default top padding */
    .block-container { padding-top: 0 !important; padding-bottom: 40px !important; }
    .stMainBlockContainer { padding-top: 0 !important; }

    /* ── NAV BAR ── */
    .nav-container {
        background: #FAF8F5;
        border-bottom: 2px solid #2C2C2C;
        padding: 20px 0 0 0;
        margin-bottom: 32px;
    }
    .nav-wordmark {
        font-family: 'Source Serif 4', serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #888580;
        margin-bottom: 16px;
    }

    /* Override ALL Streamlit button styles for nav */
    div[data-testid="stHorizontalBlock"] .stButton > button {
        background: transparent !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        border-radius: 0 !important;
        color: #888580 !important;
        font-family: 'Source Serif 4', serif !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        letter-spacing: 0.04em !important;
        padding: 8px 4px 12px 4px !important;
        margin: 0 !important;
        box-shadow: none !important;
        transition: color 0.15s ease, border-color 0.15s ease !important;
        width: 100% !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        background: transparent !important;
        color: #2C2C2C !important;
        border-bottom: 3px solid #40826D !important;
        box-shadow: none !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton[data-active="true"] > button,
    div[data-testid="stHorizontalBlock"] .stButton > button[kind="primary"] {
        background: transparent !important;
        color: #2C2C2C !important;
        font-weight: 600 !important;
        border-bottom: 3px solid #40826D !important;
        box-shadow: none !important;
    }

   /* ── SELECTBOX / MULTISELECT — light theme ── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D0CCC7 !important;
        border-radius: 2px !important;
        color: #2C2C2C !important;
        font-family: 'Source Serif 4', serif !important;
        font-size: 14px !important;
    }
    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within {
        border-color: #40826D !important;
        box-shadow: 0 0 0 1px #40826D !important;
    }
    .stSelectbox label, .stMultiSelect label {
        font-family: 'Source Serif 4', serif !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: #888580 !important;
    }

    /* Dropdown portal — light theme (fixes dark hover) */
    [data-baseweb="popover"] {
        background-color: #FFFFFF !important;
    }
    [data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E4E0DA !important;
        border-radius: 2px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }
    [data-baseweb="menu"] li {
        background-color: #FFFFFF !important;
        color: #2C2C2C !important;
        font-family: 'Source Serif 4', serif !important;
        font-size: 13.5px !important;
    }
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #F2F7F5 !important;
        color: #2C2C2C !important;
    }
    [data-baseweb="menu"] li[aria-selected="true"] {
        font-weight: 600 !important;
    }

    /* Multiselect tags */
    [data-baseweb="tag"] {
        background-color: #E8F2EE !important;
        border: 1px solid #40826D !important;
        border-radius: 2px !important;
    }
    [data-baseweb="tag"] span {
        color: #2C2C2C !important;
        font-family: 'Source Serif 4', serif !important;
        font-size: 12px !important;
    }
    [data-baseweb="tag"] [role="presentation"] {
        color: #40826D !important;
    }

    /* Light tooltip */
    [data-baseweb="tooltip"],
    .stTooltipContent {
        background-color: #FFFFFF !important;
        color: #2C2C2C !important;
        border: 1px solid #E4E0DA !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }

    /* ── METRIC CARDS ── */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E4E0DA;
        border-top: 3px solid #40826D;
        padding: 22px 26px;
        height: 100%;
    }
    .metric-label {
        font-family: 'Source Serif 4', serif;
        font-size: 10.5px;
        font-weight: 600;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        color: #888580;
        margin-bottom: 10px;
    }
    .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 30px;
        font-weight: 700;
        color: #2C2C2C;
        line-height: 1.1;
    }
    .metric-sub {
        font-family: 'Source Serif 4', serif;
        font-size: 12px;
        color: #AAA69F;
        margin-top: 7px;
        font-style: italic;
    }

    /* ── SECTION HEADERS ── */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 20px;
        font-weight: 600;
        color: #2C2C2C;
        margin: 36px 0 6px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid #E4E0DA;
    }
    .section-number {
        color: #40826D;
        font-style: italic;
        font-size: 15px;
        margin-right: 8px;
        font-weight: 400;
    }

    /* ── PAGE TITLES ── */
    .page-title {
        font-family: 'Playfair Display', serif;
        font-size: 34px;
        font-weight: 700;
        color: #2C2C2C;
        margin: 0 0 6px 0;
        line-height: 1.2;
    }
    .page-subtitle {
        font-family: 'Source Serif 4', serif;
        font-size: 14px;
        color: #888580;
        font-style: italic;
        margin-bottom: 28px;
        line-height: 1.5;
    }

    /* ── FIGURE CAPTIONS ── */
    .figure-caption {
        font-family: 'Source Serif 4', serif;
        font-size: 12.5px;
        color: #6A6660;
        font-style: italic;
        margin-top: 8px;
        padding: 10px 0 18px 0;
        border-bottom: 1px solid #E4E0DA;
        line-height: 1.55;
    }
    .figure-label {
        font-weight: 600;
        font-style: normal;
        color: #40826D;
    }
    .data-source {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #B0ACA6;
        letter-spacing: 0.04em;
    }

    /* ── INSIGHT BOX ── */
    .insight-box {
        background: #F2F7F5;
        border-left: 3px solid #40826D;
        padding: 14px 20px;
        margin: 18px 0 24px 0;
        font-family: 'Source Serif 4', serif;
        font-size: 13.5px;
        color: #2C2C2C;
        line-height: 1.65;
    }
    .insight-box strong { color: #40826D; }

    /* ── DATAFRAME TABLE ── */
    .stDataFrame { font-size: 13px !important; }
    .stDataFrame thead th {
        font-family: 'Source Serif 4', serif !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #888580 !important;
        background: #F5F3F0 !important;
    }

    /* ── HIDE STREAMLIT CHROME ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* ── PLOTLY TOOLBAR ── */
    .modebar { opacity: 0.3 !important; }
    .modebar:hover { opacity: 1 !important; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# DESIGN TOKENS
# -------------------------------------------------------
C = {
    "primary":   "#40826D",
    "secondary": "#E89EB8",
    "dark":      "#2C2C2C",
    "gray":      "#888580",
    "light":     "#E4E0DA",
    "bg":        "#FAF8F5",
    "white":     "#FFFFFF",
    "amber":     "#C9822A",
    "p_light":   "#6FAF97",
    "s_light":   "#F2C4D5",
}
FONT       = "Source Serif 4, Georgia, serif"
TITLE_FONT = "Playfair Display, Georgia, serif"

# -------------------------------------------------------
# LAYOUT HELPERS
# -------------------------------------------------------
def chart_layout(fig, title, xtitle="", ytitle="", height=420, show_x_grid=True):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family=TITLE_FONT, size=14, color=C["dark"]),
            x=0, xanchor="left", pad=dict(b=14, l=2)
        ),
        plot_bgcolor=C["white"],
        paper_bgcolor=C["bg"],
        font=dict(family=FONT, color=C["dark"], size=12),
        height=height,
        margin=dict(l=8, r=16, t=56, b=8),
        xaxis=dict(
            title=dict(text=xtitle, font=dict(size=11, color=C["gray"])),
            showgrid=show_x_grid, gridcolor=C["light"], gridwidth=1,
            showline=True, linecolor=C["light"], linewidth=1,
            tickfont=dict(size=11, color=C["dark"]),
            automargin=True,
        ),
        yaxis=dict(
            title=dict(text=ytitle, font=dict(size=11, color=C["gray"])),
            showgrid=True, gridcolor=C["light"], gridwidth=1,
            showline=False,
            tickfont=dict(size=11, color=C["dark"]),
            automargin=True,
        ),
        legend=dict(
            font=dict(size=11, family=FONT),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
        ),
        hovermode="x unified",
    )
    return fig

def caption(label, text, source="Zillow Research · U.S. Census Bureau ACS · FRED"):
    st.markdown(
        f'<p class="figure-caption">'
        f'<span class="figure-label">{label}</span> — {text} '
        f'<span class="data-source">// {source}</span></p>',
        unsafe_allow_html=True
    )

def section(number, title):
    st.markdown(
        f'<p class="section-header">'
        f'<span class="section-number">{number}</span>{title}</p>',
        unsafe_allow_html=True
    )

def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def page_header(title, subtitle):
    st.markdown(f'<p class="page-title">{title}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)

# -------------------------------------------------------
# DATA HELPERS
# -------------------------------------------------------
@st.cache_data(ttl=3600)
def get_cities():
    df = run_query("SELECT DISTINCT city FROM cities ORDER BY city")
    return df["city"].tolist()

@st.cache_data(ttl=3600)
def get_overview_metrics():
    total   = run_query("SELECT COUNT(*) as cnt FROM cities").iloc[0]["cnt"]
    latest  = run_query("SELECT MAX(date) as d FROM home_prices").iloc[0]["d"]
    avg_r   = run_query("""
        SELECT ROUND(AVG(hp.median_home_value / il.median_household_income), 2) as r
        FROM home_prices hp
        JOIN cities c ON hp.city_id = c.city_id
        JOIN income_levels il ON c.city_id = il.city_id AND YEAR(hp.date) = il.year
        WHERE il.year = 2023
    """).iloc[0]["r"]
    return total, latest, avg_r

YEAR_OPTIONS = [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015]

# -------------------------------------------------------
# NAVIGATION
# -------------------------------------------------------
st.markdown('<div class="nav-container"><div class="nav-wordmark">U.S. Housing Market Intelligence Platform</div></div>', unsafe_allow_html=True)

PAGES = ["Market Overview", "City Explorer", "Price Trends", "Speculation Index", "Rent vs. Buy", "Data Explorer"]

if "page" not in st.session_state:
    st.session_state.page = "Market Overview"

nav_cols = st.columns(len(PAGES))
for i, p in enumerate(PAGES):
    with nav_cols[i]:
        is_active = st.session_state.page == p
        if st.button(p, key=f"nav_{p}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.page = p
            st.rerun()

st.markdown("<hr style='margin:0 0 28px 0; border:none; border-top:2px solid #2C2C2C;'>", unsafe_allow_html=True)
page = st.session_state.page

# ================================================================
# PAGE 1 — MARKET OVERVIEW
# ================================================================
if page == "Market Overview":
    page_header(
        "U.S. Housing Market Overview",
        "A cross-sectional analysis of affordability, rent burden, and market stress across U.S. metropolitan areas."
    )

    total, latest, avg_r = get_overview_metrics()
    c1, c2, c3 = st.columns(3)
    for col, label, val, sub in [
        (c1, "Metropolitan Areas Tracked",     f"{total:,}",             "U.S. metros and micropolitans"),
        (c2, "Most Recent Observation",         str(latest)[:7],          "Zillow Home Value Index (ZHVI)"),
        (c3, "National Avg. Price-to-Income",   f"{avg_r}x",              "Across tracked metros, 2023"),
    ]:
        with col:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    insight("<strong>How to read this dashboard:</strong> A price-to-income ratio above 5.0x is broadly considered unaffordable by housing economists. A rent-to-income ratio exceeding 30% defines rent burden per the U.S. Department of Housing and Urban Development (HUD). Both thresholds are marked on relevant figures throughout.")

    section("1.1", "Affordability Rankings")

    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        year = st.selectbox("Reference Year", YEAR_OPTIONS, index=0, key="ov_year")
    with f_col2:
        top_n = st.selectbox("Cities to display", [10, 20, 30], index=1, key="ov_n")
    with f_col3:
        sort_dir = st.selectbox("Sort Order", ["Least Affordable First", "Most Affordable First"], key="ov_sort")

    rankings = run_query(f"""
        SELECT c.city, c.state,
            ROUND(AVG(hp.median_home_value), 0)   AS avg_home_value,
            il.median_household_income             AS median_income,
            ROUND(AVG(hp.median_home_value) / il.median_household_income, 2) AS price_to_income_ratio
        FROM home_prices hp
        JOIN cities c ON hp.city_id = c.city_id
        JOIN income_levels il ON c.city_id = il.city_id AND YEAR(hp.date) = il.year
        WHERE il.year = {year}
        GROUP BY c.city_id, c.city, c.state, il.median_household_income
        ORDER BY price_to_income_ratio {'DESC' if sort_dir == 'Least Affordable First' else 'ASC'}
        LIMIT {top_n}
    """)

    if not rankings.empty:
        fig = go.Figure(go.Bar(
            x=rankings["price_to_income_ratio"],
            y=rankings["city"],
            orientation="h",
            marker=dict(
                color=rankings["price_to_income_ratio"],
                colorscale=[[0, C["primary"]], [0.45, C["amber"]], [1, C["secondary"]]],
                showscale=False,
            ),
            customdata=rankings[["avg_home_value", "median_income"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Price-to-Income: %{x:.2f}x<br>"
                "Avg Home Value: $%{customdata[0]:,.0f}<br>"
                "Median Income: $%{customdata[1]:,.0f}"
                "<extra></extra>"
            )
        ))
        fig.add_vline(x=5.0, line_dash="dot", line_color=C["dark"], line_width=1,
                      annotation_text="5.0x threshold",
                      annotation_font_size=10, annotation_font_color=C["gray"],
                      annotation_position="top right")
        fig = chart_layout(
            fig,
            f"Figure 1.1 — Price-to-Income Ratio, {top_n} Least Affordable Metros ({year})",
            xtitle="Price-to-Income Ratio",
            height=max(380, top_n * 22 + 100)
        )
        fig.update_layout(
            yaxis=dict(autorange="reversed" if sort_dir == "Least Affordable First" else True, automargin=True),
            margin=dict(l=180, r=24, t=56, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)
        caption("Figure 1.1",
                f"Horizontal bars represent the ratio of average annual median home value to median household income for {year}. "
                f"Color gradient transitions from green (lower ratio) through amber to pink (higher ratio). "
                f"The dotted vertical line marks the 5.0x threshold commonly used by housing economists to define unaffordability.")

    section("1.2", "Composite Market Stress Landscape")

    year2 = st.selectbox("Reference Year", YEAR_OPTIONS, index=0, key="ov_stress_year")
    stress = run_query(f"""
        WITH affordability AS (
            SELECT c.city_id, c.city, c.state,
                ROUND(AVG(hp.median_home_value) / il.median_household_income, 2) AS ptr
            FROM home_prices hp JOIN cities c ON hp.city_id = c.city_id
            JOIN income_levels il ON c.city_id = il.city_id AND YEAR(hp.date) = il.year
            WHERE il.year = {year2}
            GROUP BY c.city_id, c.city, c.state, il.median_household_income
        ),
        rent_burden AS (
            SELECT c.city_id,
                ROUND((AVG(rp.median_rent) * 12) / il.median_household_income * 100, 2) AS rtr
            FROM rent_prices rp JOIN cities c ON rp.city_id = c.city_id
            JOIN income_levels il ON c.city_id = il.city_id AND YEAR(rp.date) = il.year
            WHERE il.year = {year2}
            GROUP BY c.city_id, il.median_household_income
        ),
        price_growth AS (
            SELECT city_id, city, price_growth_yoy_pct FROM (
                SELECT c.city_id, c.city, YEAR(hp.date) AS yr,
                    ROUND((AVG(hp.median_home_value) - LAG(AVG(hp.median_home_value))
                        OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)))
                        / LAG(AVG(hp.median_home_value))
                        OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)) * 100, 2) AS price_growth_yoy_pct
                FROM home_prices hp JOIN cities c ON hp.city_id = c.city_id
                GROUP BY c.city_id, c.city, YEAR(hp.date)
            ) g WHERE yr = {year2}
        )
        SELECT a.city, a.state,
            a.ptr                                                        AS price_to_income,
            rb.rtr                                                       AS rent_to_income_pct,
            pg.price_growth_yoy_pct,
            ROUND((a.ptr * 0.5) + (rb.rtr / 10 * 0.3) + (pg.price_growth_yoy_pct * 0.2), 2) AS stress_score,
            CASE
                WHEN ROUND((a.ptr*0.5)+(rb.rtr/10*0.3)+(pg.price_growth_yoy_pct*0.2),2) > 7 THEN 'High Stress'
                WHEN ROUND((a.ptr*0.5)+(rb.rtr/10*0.3)+(pg.price_growth_yoy_pct*0.2),2) > 4 THEN 'Moderate Stress'
                ELSE 'Affordable'
            END AS market_status
        FROM affordability a
        JOIN rent_burden rb ON a.city_id = rb.city_id
        JOIN price_growth pg ON a.city_id = pg.city_id
        ORDER BY stress_score DESC
        LIMIT 40
    """)

    if not stress.empty:
        color_map = {
            "High Stress":     C["secondary"],
            "Moderate Stress": C["amber"],
            "Affordable":      C["primary"],
        }
        fig2 = px.scatter(
            stress,
            x="price_to_income", y="rent_to_income_pct",
            size="stress_score",
            color="market_status",
            color_discrete_map=color_map,
            hover_name="city",
            custom_data=["state", "stress_score", "price_growth_yoy_pct"],
            size_max=30,
        )
        fig2.update_traces(
            hovertemplate=(
                "<b>%{hovertext}, %{customdata[0]}</b><br>"
                "Price-to-Income: %{x:.2f}x<br>"
                "Rent-to-Income: %{y:.1f}%<br>"
                "Stress Score: %{customdata[1]:.2f}<br>"
                "Price Growth YoY: %{customdata[2]:.1f}%"
                "<extra></extra>"
            )
        )
        fig2.add_hline(y=30, line_dash="dot", line_color=C["dark"], line_width=1,
                       annotation_text="30% rent burden threshold",
                       annotation_font_size=10, annotation_font_color=C["gray"],
                       annotation_position="bottom right")
        fig2.add_vline(x=5.0, line_dash="dot", line_color=C["dark"], line_width=1,
                       annotation_text="5.0x price threshold",
                       annotation_font_size=10, annotation_font_color=C["gray"],
                       annotation_position="top left")
        fig2 = chart_layout(
            fig2,
            f"Figure 1.2 — Market Stress Landscape ({year2}): Price-to-Income vs. Rent Burden",
            xtitle="Price-to-Income Ratio",
            ytitle="Annual Rent as % of Median Income",
            height=500,
        )
        fig2.update_layout(
            legend=dict(title="Market Classification", orientation="v",
                        yanchor="top", y=0.98, xanchor="left", x=0.01,
                        bgcolor="rgba(255,255,255,0.85)", bordercolor=C["light"], borderwidth=1),
        )
        st.plotly_chart(fig2, use_container_width=True)
        caption("Figure 1.2",
                f"Each bubble represents a metropolitan area. Bubble size corresponds to the composite market stress score "
                f"(weighted: 50% price-to-income, 30% rent burden, 20% price growth). "
                f"Dotted lines mark standard affordability thresholds. "
                f"Markets in the upper-right quadrant face simultaneous home value and rent burden pressure.")

# ================================================================
# PAGE 2 — CITY EXPLORER
# ================================================================
elif page == "City Explorer":
    page_header(
        "City Explorer",
        "Detailed affordability profile and trend analysis for individual metropolitan statistical areas."
    )

    cities = get_cities()
    f1, f2 = st.columns([3, 1])
    with f1:
        selected = st.selectbox(
            "Select Metropolitan Area", cities,
            index=cities.index("Austin, TX") if "Austin, TX" in cities else 0,
            key="ce_city"
        )
    with f2:
        year_sel = st.selectbox("Reference Year", YEAR_OPTIONS, index=0, key="ce_year")

    # Key metrics
    metrics = run_query(f"""
        SELECT ROUND(AVG(hp.median_home_value), 0) AS avg_price,
               il.median_household_income           AS income,
               ROUND(AVG(hp.median_home_value) / il.median_household_income, 2) AS ptr
        FROM home_prices hp
        JOIN cities c ON hp.city_id = c.city_id
        JOIN income_levels il ON c.city_id = il.city_id AND YEAR(hp.date) = il.year
        WHERE c.city = '{selected}' AND il.year = {year_sel}
        GROUP BY il.median_household_income
    """)
    rent_m = run_query(f"""
        SELECT ROUND(AVG(rp.median_rent), 0) AS avg_rent,
               ROUND((AVG(rp.median_rent) * 12) / il.median_household_income * 100, 1) AS rtr
        FROM rent_prices rp
        JOIN cities c ON rp.city_id = c.city_id
        JOIN income_levels il ON c.city_id = il.city_id AND YEAR(rp.date) = il.year
        WHERE c.city = '{selected}' AND il.year = {year_sel}
        GROUP BY il.median_household_income
    """)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    mc = st.columns(4)
    if not metrics.empty:
        m = metrics.iloc[0]
        ptr_flag = "Above 5.0x threshold" if m["ptr"] > 5 else "Below 5.0x threshold"
        with mc[0]:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Median Home Value</div>
                <div class="metric-value">${m['avg_price']:,.0f}</div>
                <div class="metric-sub">{year_sel} annual average</div>
            </div>""", unsafe_allow_html=True)
        with mc[1]:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Median Household Income</div>
                <div class="metric-value">${m['income']:,.0f}</div>
                <div class="metric-sub">{year_sel} ACS estimate</div>
            </div>""", unsafe_allow_html=True)
        with mc[2]:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Price-to-Income Ratio</div>
                <div class="metric-value">{m['ptr']}x</div>
                <div class="metric-sub">{ptr_flag}</div>
            </div>""", unsafe_allow_html=True)
        if not rent_m.empty:
            r = rent_m.iloc[0]
            burden = "Rent burdened (>30%)" if r["rtr"] > 30 else "Below burden threshold"
            with mc[3]:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">Rent-to-Income Ratio</div>
                    <div class="metric-value">{r['rtr']}%</div>
                    <div class="metric-sub">{burden}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # 2.1 Affordability trend
    section("2.1", "Price-to-Income Ratio Over Time")
    trend = run_query(f"""
        SELECT il.year,
               ROUND(AVG(hp.median_home_value), 0)  AS avg_price,
               il.median_household_income            AS income,
               ROUND(AVG(hp.median_home_value) / il.median_household_income, 2) AS ptr
        FROM home_prices hp
        JOIN cities c ON hp.city_id = c.city_id
        JOIN income_levels il ON c.city_id = il.city_id AND YEAR(hp.date) = il.year
        WHERE c.city = '{selected}'
        GROUP BY il.year, il.median_household_income
        ORDER BY il.year
    """)

    if not trend.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend["year"], y=trend["ptr"],
            mode="lines+markers",
            name="Price-to-Income Ratio",
            line=dict(color=C["primary"], width=2.5),
            marker=dict(size=8, color=C["primary"], line=dict(color=C["white"], width=1.5)),
            hovertemplate="<b>%{x}</b><br>Ratio: %{y:.2f}x<extra></extra>"
        ))
        fig.add_hline(y=5.0, line_dash="dot", line_color=C["dark"], line_width=1,
                      annotation_text="5.0x threshold", annotation_font_size=10,
                      annotation_font_color=C["gray"], annotation_position="bottom right")
        fig = chart_layout(fig, f"Figure 2.1 — Annual Price-to-Income Ratio: {selected}",
                           xtitle="Year", ytitle="Price-to-Income Ratio", height=360)
        st.plotly_chart(fig, use_container_width=True)
        caption("Figure 2.1",
                f"Annual price-to-income ratio for {selected}, 2015–2024. "
                f"Derived from Zillow ZHVI annual averages divided by U.S. Census ACS median household income. "
                f"Values above the dotted line indicate unaffordability by conventional standards.")

    # 2.2 Home value vs income
    section("2.2", "Home Value vs. Household Income")
    if not trend.empty:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=trend["year"], y=trend["avg_price"],
            name="Median Home Value",
            marker_color=C["primary"], opacity=0.80,
            hovertemplate="<b>%{x}</b><br>Home Value: $%{y:,.0f}<extra></extra>"
        ))
        fig2.add_trace(go.Scatter(
            x=trend["year"], y=trend["income"],
            name="Median Household Income",
            yaxis="y2",
            line=dict(color=C["secondary"], width=2.5, dash="dash"),
            marker=dict(size=7, color=C["secondary"]),
            mode="lines+markers",
            hovertemplate="<b>%{x}</b><br>Income: $%{y:,.0f}<extra></extra>"
        ))
        fig2.update_layout(
            yaxis=dict(title=dict(text="Median Home Value (USD)", font=dict(size=11)),
                       tickprefix="$", automargin=True),
            yaxis2=dict(overlaying="y", side="right", showgrid=False,
                        tickprefix="$", tickfont=dict(size=11),
                        title=dict(text="Median Household Income (USD)", font=dict(size=11)),
                        automargin=True),
            legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="left", x=0),
        )
        fig2 = chart_layout(fig2, f"Figure 2.2 — Median Home Value vs. Household Income: {selected}",
                            xtitle="Year", ytitle="", height=400)
        st.plotly_chart(fig2, use_container_width=True)
        caption("Figure 2.2",
                f"Green bars represent average annual median home values (left axis). "
                f"Dashed pink line represents median household income (right axis). "
                f"Divergence between the two series indicates growing affordability pressure independent of income gains.")

    # 2.3 Monthly price history
    section("2.3", "Monthly Home Value History")
    monthly = run_query(f"""
        SELECT hp.date, hp.median_home_value,
               ROUND(AVG(hp.median_home_value) OVER (
                   PARTITION BY c.city_id ORDER BY hp.date
                   ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
               ), 0) AS rolling_12mo
        FROM home_prices hp
        JOIN cities c ON hp.city_id = c.city_id
        WHERE c.city = '{selected}'
        ORDER BY hp.date
    """)
    if not monthly.empty:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=monthly["date"], y=monthly["median_home_value"],
            mode="lines", name="Monthly Value",
            line=dict(color=C["light"], width=1.5),
            hovertemplate="<b>%{x|%b %Y}</b><br>Monthly: $%{y:,.0f}<extra></extra>"
        ))
        fig3.add_trace(go.Scatter(
            x=monthly["date"], y=monthly["rolling_12mo"],
            mode="lines", name="12-Month Rolling Avg.",
            line=dict(color=C["primary"], width=2.5),
            hovertemplate="<b>%{x|%b %Y}</b><br>12-Mo Avg: $%{y:,.0f}<extra></extra>"
        ))
        fig3 = chart_layout(fig3, f"Figure 2.3 — Monthly Home Value with 12-Month Rolling Average: {selected}",
                            xtitle="Date", ytitle="Median Home Value (USD)", height=380)
        fig3.update_layout(yaxis=dict(tickprefix="$"),
                           legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="left", x=0))
        st.plotly_chart(fig3, use_container_width=True)
        caption("Figure 2.3",
                f"Light gray line shows raw monthly ZHVI values for {selected}. "
                f"Green line shows the trailing 12-month rolling average, which attenuates seasonal noise to reveal the underlying trend.")

# ================================================================
# PAGE 3 — PRICE TRENDS
# ================================================================
elif page == "Price Trends":
    page_header(
        "Price Trends",
        "Comparative monthly home value trajectories, rolling averages, and annual growth rates across selected metropolitan areas."
    )

    cities = get_cities()
    f1, f2 = st.columns([3, 1])
    with f1:
        selected_cities = st.multiselect(
            "Select Metropolitan Areas (2–6)",
            cities,
            default=["Austin, TX", "Miami, FL", "Minneapolis, MN"],
            max_selections=6,
            key="pt_cities"
        )
    with f2:
        start_year = st.selectbox("Start Year", [2015,2016,2017,2018,2019,2020], index=0, key="pt_start")

    if not selected_cities:
        st.info("Select at least one metropolitan area to display charts.")
        st.stop()

    city_list  = ", ".join([f"'{c}'" for c in selected_cities])
    COLOR_SEQ  = [C["primary"], C["secondary"], C["amber"], "#6B8CAE", "#9B7EBD", "#8B7355"]

    section("3.1", "Monthly Median Home Value")
    prices = run_query(f"""
        SELECT c.city, hp.date, hp.median_home_value
        FROM home_prices hp JOIN cities c ON hp.city_id = c.city_id
        WHERE c.city IN ({city_list}) AND hp.date >= '{start_year}-01-01'
        ORDER BY c.city, hp.date
    """)
    if not prices.empty:
        fig = px.line(prices, x="date", y="median_home_value", color="city",
                      color_discrete_sequence=COLOR_SEQ,
                      labels={"date": "Date", "median_home_value": "Median Home Value (USD)", "city": "Metro Area"})
        fig.update_traces(line_width=2,
                          hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>")
        fig = chart_layout(fig, "Figure 3.1 — Monthly Median Home Value by Metropolitan Area",
                           xtitle="Date", ytitle="Median Home Value (USD)", height=440)
        fig.update_layout(yaxis=dict(tickprefix="$"),
                          legend=dict(title="Metro Area", orientation="h",
                                      yanchor="bottom", y=1.04, xanchor="left", x=0))
        st.plotly_chart(fig, use_container_width=True)
        caption("Figure 3.1",
                "Monthly smoothed median home values from the Zillow Home Value Index (ZHVI), seasonally adjusted. "
                "Each series represents a distinct metropolitan statistical area.")

    section("3.2", "12-Month Rolling Average")
    rolling = run_query(f"""
        SELECT c.city, hp.date,
               ROUND(AVG(hp.median_home_value) OVER (
                   PARTITION BY c.city_id ORDER BY hp.date
                   ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
               ), 0) AS rolling_avg
        FROM home_prices hp JOIN cities c ON hp.city_id = c.city_id
        WHERE c.city IN ({city_list}) AND hp.date >= '{start_year}-01-01'
        ORDER BY c.city, hp.date
    """)
    if not rolling.empty:
        fig2 = px.line(rolling, x="date", y="rolling_avg", color="city",
                       color_discrete_sequence=COLOR_SEQ,
                       labels={"date": "Date", "rolling_avg": "Rolling Avg. Home Value (USD)", "city": "Metro Area"})
        fig2.update_traces(line_width=2,
                           hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>")
        fig2 = chart_layout(fig2, "Figure 3.2 — 12-Month Rolling Average Home Value by Metropolitan Area",
                            xtitle="Date", ytitle="Rolling Avg. Home Value (USD)", height=440)
        fig2.update_layout(yaxis=dict(tickprefix="$"),
                           legend=dict(title="Metro Area", orientation="h",
                                       yanchor="bottom", y=1.04, xanchor="left", x=0))
        st.plotly_chart(fig2, use_container_width=True)
        caption("Figure 3.2",
                "Trailing 12-month rolling average. Attenuates seasonal fluctuations to expose the underlying trend. "
                "First 11 months of each series use a partial window.")

    section("3.3", "Year-Over-Year Price Growth (%)")
    growth = run_query(f"""
        SELECT city, year, yoy_growth FROM (
            SELECT c.city, YEAR(hp.date) AS year,
                ROUND((AVG(hp.median_home_value) - LAG(AVG(hp.median_home_value))
                    OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)))
                    / LAG(AVG(hp.median_home_value))
                    OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)) * 100, 2) AS yoy_growth
            FROM home_prices hp JOIN cities c ON hp.city_id = c.city_id
            WHERE c.city IN ({city_list})
            GROUP BY c.city_id, c.city, YEAR(hp.date)
        ) g WHERE yoy_growth IS NOT NULL AND year >= {start_year}
        ORDER BY city, year
    """)
    if not growth.empty:
        fig3 = px.line(growth, x="year", y="yoy_growth", color="city",
                       markers=True, color_discrete_sequence=COLOR_SEQ,
                       labels={"year": "Year", "yoy_growth": "YoY Growth (%)", "city": "Metro Area"})
        fig3.update_traces(line_width=2, marker_size=7,
                           hovertemplate="<b>%{x}</b><br>Growth: %{y:.2f}%<extra></extra>")
        fig3.add_hline(y=0, line_color=C["dark"], line_width=1)
        fig3 = chart_layout(fig3, "Figure 3.3 — Annual Year-Over-Year Home Price Growth Rate (%)",
                            xtitle="Year", ytitle="YoY Growth (%)", height=420)
        fig3.update_layout(yaxis=dict(ticksuffix="%"),
                           legend=dict(title="Metro Area", orientation="h",
                                       yanchor="bottom", y=1.04, xanchor="left", x=0))
        st.plotly_chart(fig3, use_container_width=True)
        caption("Figure 3.3",
                "Year-over-year percentage change in annual average median home value. "
                "Computed using the LAG() window function against the prior year's annual average. "
                "Values below zero indicate year-over-year price decline.")

# ================================================================
# PAGE 4 — SPECULATION INDEX
# ================================================================
elif page == "Speculation Index":
    page_header(
        "Speculation Index",
        "Measuring divergence between home price appreciation and income growth as an indicator of speculative market conditions."
    )

    insight("<strong>Methodology:</strong> The Speculation Index is defined as the difference in percentage points between annual home price growth and annual household income growth. A large positive index suggests prices are appreciating faster than local economic fundamentals can sustain — a condition historically associated with elevated correction risk. Values near zero or negative indicate price growth broadly in line with income growth.")

    f1, f2 = st.columns([2, 1])
    with f1:
        year = st.selectbox("Reference Year", YEAR_OPTIONS, index=1, key="si_year")
    with f2:
        top_n = st.selectbox("Cities to display", [15, 25, 40], index=1, key="si_n")

    spec = run_query(f"""
        SELECT pd.city, pd.state,
               pd.price_growth_yoy_pct,
               id2.income_growth_yoy_pct,
               ROUND(pd.price_growth_yoy_pct - id2.income_growth_yoy_pct, 2) AS speculation_index
        FROM (
            SELECT c.city_id, c.city, c.state, YEAR(hp.date) AS yr,
                ROUND((AVG(hp.median_home_value) - LAG(AVG(hp.median_home_value))
                    OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)))
                    / LAG(AVG(hp.median_home_value))
                    OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)) * 100, 2) AS price_growth_yoy_pct
            FROM home_prices hp JOIN cities c ON hp.city_id = c.city_id
            GROUP BY c.city_id, c.city, c.state, YEAR(hp.date)
        ) pd
        JOIN (
            SELECT city_id, year,
                ROUND((median_household_income - LAG(median_household_income)
                    OVER (PARTITION BY city_id ORDER BY year))
                    / LAG(median_household_income)
                    OVER (PARTITION BY city_id ORDER BY year) * 100, 2) AS income_growth_yoy_pct
            FROM income_levels
        ) id2 ON pd.city_id = id2.city_id AND pd.yr = id2.year
        WHERE pd.price_growth_yoy_pct IS NOT NULL AND id2.income_growth_yoy_pct IS NOT NULL
        ORDER BY speculation_index DESC
        LIMIT {top_n}
    """)

    section("4.1", "Speculation Index Rankings")
    if not spec.empty:
        s_max = spec["speculation_index"].max()
        s_p75 = spec["speculation_index"].quantile(0.75)
        s_p40 = spec["speculation_index"].quantile(0.40)

        def spec_color(v):
            if v >= s_p75:   return C["secondary"]
            elif v >= s_p40:  return C["amber"]
            elif v >= 0: return C["p_light"]
            else:        return C["primary"]

        spec["bar_color"] = spec["speculation_index"].apply(spec_color)

        fig = go.Figure(go.Bar(
            x=spec["speculation_index"],
            y=spec["city"],
            orientation="h",
            marker_color=spec["bar_color"],
            customdata=spec[["price_growth_yoy_pct", "income_growth_yoy_pct"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Speculation Index: %{x:.2f}pp<br>"
                "Price Growth: %{customdata[0]:.2f}%<br>"
                "Income Growth: %{customdata[1]:.2f}%"
                "<extra></extra>"
            )
        ))
        fig.add_vline(x=0, line_color=C["dark"], line_width=1.5)
        fig = chart_layout(
            fig,
            f"Figure 4.1 — Speculation Index by Metropolitan Area ({year})",
            xtitle="Speculation Index (Price Growth % − Income Growth %)",
            height=max(420, top_n * 20 + 120)
        )
        fig.update_layout(
            yaxis=dict(autorange="reversed", automargin=True),
            margin=dict(l=180, r=24, t=56, b=40), 
            hoverlabel=dict(
                bgcolor=C["white"],
                bordercolor=C["light"],
                font=dict(family=FONT, size=12, color=C["dark"]),
        ),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div style='display:flex; gap:24px; margin:8px 0 4px 0; font-family:"Source Serif 4",serif; font-size:12px; color:#2C2C2C;'>
            <span><span style='display:inline-block;width:12px;height:12px;background:#E89EB8;margin-right:6px;'></span>High speculative pressure (&gt;15pp)</span>
            <span><span style='display:inline-block;width:12px;height:12px;background:#C9822A;margin-right:6px;'></span>Moderate divergence (5–15pp)</span>
            <span><span style='display:inline-block;width:12px;height:12px;background:#6FAF97;margin-right:6px;'></span>Low divergence (0–5pp)</span>
            <span><span style='display:inline-block;width:12px;height:12px;background:#40826D;margin-right:6px;'></span>Prices trailing income (&lt;0)</span>
        </div>
        """, unsafe_allow_html=True)
        caption("Figure 4.1",
                f"Bars represent the difference in percentage points between annual home price growth and annual household income growth in {year}. "
                f"Color intensity reflects the magnitude of speculative pressure. "
                f"Negative values indicate markets where incomes grew faster than home prices.")

    section("4.2", "Price Growth vs. Income Growth")
    if not spec.empty:
        rng = max(abs(spec["price_growth_yoy_pct"].max()),
                  abs(spec["price_growth_yoy_pct"].min()),
                  abs(spec["income_growth_yoy_pct"].max()),
                  abs(spec["income_growth_yoy_pct"].min())) * 1.1

        fig2 = px.scatter(
            spec, x="income_growth_yoy_pct", y="price_growth_yoy_pct",
            hover_name="city",
            color="speculation_index",
            color_continuous_scale=[[0, C["primary"]], [0.4, C["p_light"]], [0.65, C["amber"]], [1, C["secondary"]]],
            size=spec["speculation_index"].clip(lower=0.1),
            size_max=20,
            labels={
                "income_growth_yoy_pct": "Income Growth YoY (%)",
                "price_growth_yoy_pct":  "Price Growth YoY (%)",
                "speculation_index":     "Speculation Index",
            }
        )
        fig2.update_traces(
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Price Growth: %{y:.2f}%<br>"
                "Income Growth: %{x:.2f}%<br>"
                "Speculation Index: %{marker.color:.2f}pp"
                "<extra></extra>"
            )
        )
        fig2.add_trace(go.Scatter(
            x=[-rng, rng], y=[-rng, rng],
            mode="lines",
            line=dict(color=C["dark"], width=1, dash="dot"),
            name="Parity (price growth = income growth)",
            showlegend=True,
        ))
        fig2 = chart_layout(
            fig2,
            f"Figure 4.2 — Price Growth vs. Income Growth Scatter ({year})",
            xtitle="Income Growth YoY (%)",
            ytitle="Home Price Growth YoY (%)",
            height=480,
        )
        fig2.update_layout(
            coloraxis_colorbar=dict(
                title=dict(text="Speculation<br>Index", font=dict(size=11)),
                tickfont=dict(size=10),
                len=0.6,
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="left", x=0),
        )
        st.plotly_chart(fig2, use_container_width=True)
        caption("Figure 4.2",
                f"Each bubble represents a metropolitan area in {year}. "
                f"Points above the parity line (dotted) indicate markets where home prices grew faster than incomes. "
                f"Distance above the line corresponds to the magnitude of divergence. "
                f"Bubble size and color both encode the speculation index.")

# ================================================================
# PAGE 5 — RENT VS BUY
# ================================================================
elif page == "Rent vs. Buy":
    page_header(
        "Rent vs. Buy Analysis",
        "Comparing monthly rental costs against estimated mortgage ownership costs across U.S. metropolitan areas."
    )

    insight("<strong>Methodology:</strong> Estimated monthly mortgage assumes a 20% down payment on the median home value, financed over 30 years at the prevailing monthly FRED 30-year fixed rate. This is a pure monthly cash-flow comparison and does not account for equity accumulation, property taxes, maintenance, insurance, or expected appreciation. A rent-to-mortgage ratio above 1.0 indicates renting is less expensive on a monthly basis.")

    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        year = st.selectbox("Reference Year", [2023,2022,2021,2020,2019,2018], index=0, key="rvb_year")
    with f2:
        show_top = st.selectbox("Show", ["All", "Rent Favored Only", "Buy Favored Only"], key="rvb_filter")
    with f3:
        top_n = st.selectbox("Cities per category", [10, 15, 20], index=1, key="rvb_n")

    rvb = run_query(f"""
        SELECT c.city, c.state,
               ROUND(AVG(rp.median_rent), 0)       AS avg_rent,
               ROUND(AVG(hp.median_home_value), 0)  AS avg_home_value,
               ROUND(AVG(ir.mortgage_rate_30yr), 4) AS avg_rate,
               ROUND(
                   (AVG(hp.median_home_value) * 0.80) *
                   (AVG(ir.mortgage_rate_30yr) / 100 / 12) /
                   (1 - POWER(1 + AVG(ir.mortgage_rate_30yr) / 100 / 12, -360))
               , 0) AS est_mortgage,
               ROUND(
                   AVG(rp.median_rent) / (
                       (AVG(hp.median_home_value) * 0.80) *
                       (AVG(ir.mortgage_rate_30yr) / 100 / 12) /
                       (1 - POWER(1 + AVG(ir.mortgage_rate_30yr) / 100 / 12, -360))
                   )
               , 2) AS rvb_ratio,
               CASE
                   WHEN AVG(rp.median_rent) / (
                       (AVG(hp.median_home_value) * 0.80) *
                       (AVG(ir.mortgage_rate_30yr) / 100 / 12) /
                       (1 - POWER(1 + AVG(ir.mortgage_rate_30yr) / 100 / 12, -360))
                   ) > 1 THEN 'Rent Favored'
                   ELSE 'Buy Favored'
               END AS recommendation
        FROM rent_prices rp
        JOIN cities c ON rp.city_id = c.city_id
        JOIN home_prices hp ON c.city_id = hp.city_id
            AND YEAR(rp.date) = YEAR(hp.date) AND MONTH(rp.date) = MONTH(hp.date)
        JOIN interest_rates ir ON YEAR(rp.date) = YEAR(ir.date)
            AND MONTH(rp.date) = MONTH(ir.date)
        WHERE YEAR(rp.date) = {year}
        GROUP BY c.city_id, c.city, c.state
        ORDER BY rvb_ratio DESC
    """)

    section("5.1", "Rent-to-Mortgage Ratio Distribution")
    if not rvb.empty:
        rent_fav = rvb[rvb["recommendation"] == "Rent Favored"].head(top_n)
        buy_fav  = rvb[rvb["recommendation"] == "Buy Favored"].tail(top_n).sort_values("rvb_ratio")

        if show_top == "Rent Favored Only":
            display = rent_fav
        elif show_top == "Buy Favored Only":
            display = buy_fav
        else:
            display = pd.concat([rent_fav, buy_fav])

        display = display.copy()
        display["bar_color"] = display["recommendation"].map({
            "Rent Favored": C["primary"],
            "Buy Favored":  C["secondary"],
        })

        fig = go.Figure(go.Bar(
            x=display["rvb_ratio"],
            y=display["city"],
            orientation="h",
            marker_color=display["bar_color"],
            customdata=display[["avg_rent", "est_mortgage", "recommendation"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Rent-to-Mortgage Ratio: %{x:.2f}<br>"
                "Avg Monthly Rent: $%{customdata[0]:,.0f}<br>"
                "Est. Monthly Mortgage: $%{customdata[1]:,.0f}<br>"
                "Classification: %{customdata[2]}"
                "<extra></extra>"
            )
        ))
        fig.add_vline(x=1.0, line_dash="dot", line_color=C["dark"], line_width=1.5,
                      annotation_text="Parity (rent = mortgage)",
                      annotation_font_size=10, annotation_font_color=C["gray"],
                      annotation_position="top right")
        fig = chart_layout(
            fig,
            f"Figure 5.1 — Rent-to-Mortgage Ratio by Metropolitan Area ({year})",
            xtitle="Monthly Rent / Estimated Monthly Mortgage",
            height=max(380, len(display) * 22 + 120)
        )
        fig.update_layout(
            yaxis=dict(autorange="reversed", automargin=True),
            margin=dict(l=180, r=24, t=56, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)
        caption("Figure 5.1",
                f"Ratio of median monthly rent to estimated monthly mortgage payment in {year}. "
                f"Green bars (ratio > 1.0) indicate markets where renting is less expensive on a monthly cash-flow basis. "
                f"Pink bars indicate markets where buying carries a lower monthly cost. "
                f"The dotted line marks cost parity.")

    section("5.2", "Rent vs. Mortgage — City Detail Over Time")
    cities = get_cities()
    f_a, f_b = st.columns([3, 1])
    with f_a:
        sel_city = st.selectbox(
            "Select Metropolitan Area", cities,
            index=cities.index("Austin, TX") if "Austin, TX" in cities else 0,
            key="rvb_city"
        )

    city_rvb = run_query(f"""
        SELECT YEAR(rp.date) AS year,
               ROUND(AVG(rp.median_rent), 0)    AS avg_rent,
               ROUND(AVG(ir.mortgage_rate_30yr), 4) AS avg_rate,
               ROUND(
                   (AVG(hp.median_home_value) * 0.80) *
                   (AVG(ir.mortgage_rate_30yr) / 100 / 12) /
                   (1 - POWER(1 + AVG(ir.mortgage_rate_30yr) / 100 / 12, -360))
               , 0) AS est_mortgage
        FROM rent_prices rp
        JOIN cities c ON rp.city_id = c.city_id
        JOIN home_prices hp ON c.city_id = hp.city_id
            AND YEAR(rp.date) = YEAR(hp.date) AND MONTH(rp.date) = MONTH(hp.date)
        JOIN interest_rates ir ON YEAR(rp.date) = YEAR(ir.date)
            AND MONTH(rp.date) = MONTH(ir.date)
        WHERE c.city = '{sel_city}'
        GROUP BY YEAR(rp.date)
        ORDER BY year
    """)

    if not city_rvb.empty:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=city_rvb["year"], y=city_rvb["avg_rent"],
            name="Median Monthly Rent",
            line=dict(color=C["primary"], width=2.5),
            marker=dict(size=8, color=C["primary"], line=dict(color=C["white"], width=1.5)),
            mode="lines+markers",
            hovertemplate="<b>%{x}</b><br>Median Rent: $%{y:,.0f}<extra></extra>"
        ))
        fig2.add_trace(go.Scatter(
            x=city_rvb["year"], y=city_rvb["est_mortgage"],
            name="Est. Monthly Mortgage",
            line=dict(color=C["secondary"], width=2.5, dash="dash"),
            marker=dict(size=8, color=C["secondary"], line=dict(color=C["white"], width=1.5)),
            mode="lines+markers",
            hovertemplate="<b>%{x}</b><br>Est. Mortgage: $%{y:,.0f}<extra></extra>"
        ))
        fig2 = chart_layout(
            fig2,
            f"Figure 5.2 — Monthly Rent vs. Estimated Mortgage: {sel_city}",
            xtitle="Year", ytitle="Monthly Cost (USD)", height=400
        )
        fig2.update_layout(
            yaxis=dict(tickprefix="$"),
            legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="left", x=0)
        )
        st.plotly_chart(fig2, use_container_width=True)
        caption("Figure 5.2",
                f"Annual average monthly rent (solid green) vs. estimated monthly mortgage payment (dashed pink) for {sel_city}. "
                f"Mortgage assumes 20% down payment at the prevailing annual average FRED 30-year fixed rate. "
                f"Periods where the dashed line exceeds the solid line indicate monthly buy costs exceed rent costs.")

# ================================================================
# PAGE 6 — DATA EXPLORER
# ================================================================
elif page == "Data Explorer":
    page_header(
        "Data Explorer",
        "Browse and filter the underlying dataset. All figures presented throughout this platform are derived from the tables below."
    )

    insight("<strong>About this data:</strong> Home value and rent data are sourced from Zillow Research (ZHVI and ZORI indices, seasonally adjusted). Income data are from the U.S. Census Bureau American Community Survey (ACS) 5-year estimates. Mortgage rate data are from the Federal Reserve Economic Data (FRED) 30-year fixed mortgage rate series.")

    table = st.selectbox(
        "Select Dataset",
        ["Home Prices", "Rent Prices", "Income Levels", "Mortgage Rates", "Affordability Summary"],
        key="de_table"
    )

    cities = get_cities()

    if table == "Home Prices":
        f1, f2, f3 = st.columns([3, 1, 1])
        with f1:
            de_cities = st.multiselect("Filter by City (leave blank for all)", cities, key="de_hp_cities")
        with f2:
            de_year_start = st.selectbox("From Year", YEAR_OPTIONS[::-1], index=0, key="de_hp_ys")
        with f3:
            de_year_end   = st.selectbox("To Year", YEAR_OPTIONS, index=0, key="de_hp_ye")

        city_clause = f"AND c.city IN ({', '.join([f'{chr(39)}{c}{chr(39)}' for c in de_cities])})" if de_cities else ""
        df = run_query(f"""
            SELECT c.city, c.state, hp.date,
                   hp.median_home_value AS `Median Home Value ($)`
            FROM home_prices hp JOIN cities c ON hp.city_id = c.city_id
            WHERE YEAR(hp.date) BETWEEN {de_year_start} AND {de_year_end}
            {city_clause}
            ORDER BY c.city, hp.date
            LIMIT 5000
        """)
        st.markdown(f"<p style='font-size:12px;color:#888580;font-family:\"Source Serif 4\",serif;'>{len(df):,} rows returned (max 5,000)</p>", unsafe_allow_html=True)
        st.dataframe(df.rename(columns={"city": "City", "state": "State", "date": "Date"}),
                     use_container_width=True, hide_index=True)

    elif table == "Rent Prices":
        f1, f2 = st.columns([3, 1])
        with f1:
            de_cities = st.multiselect("Filter by City", cities, key="de_rp_cities")
        with f2:
            de_year = st.selectbox("Year", YEAR_OPTIONS, index=0, key="de_rp_year")

        city_clause = f"AND c.city IN ({', '.join([f'{chr(39)}{c}{chr(39)}' for c in de_cities])})" if de_cities else ""
        df = run_query(f"""
            SELECT c.city, c.state, rp.date,
                   rp.median_rent AS `Median Monthly Rent ($)`
            FROM rent_prices rp JOIN cities c ON rp.city_id = c.city_id
            WHERE YEAR(rp.date) = {de_year}
            {city_clause}
            ORDER BY c.city, rp.date
            LIMIT 5000
        """)
        st.markdown(f"<p style='font-size:12px;color:#888580;font-family:\"Source Serif 4\",serif;'>{len(df):,} rows returned</p>", unsafe_allow_html=True)
        st.dataframe(df.rename(columns={"city": "City", "state": "State", "date": "Date"}),
                     use_container_width=True, hide_index=True)

    elif table == "Income Levels":
        f1, f2 = st.columns([3, 1])
        with f1:
            de_cities = st.multiselect("Filter by City", cities, key="de_il_cities")
        with f2:
            de_year = st.selectbox("Year", YEAR_OPTIONS, index=0, key="de_il_year")

        city_clause = f"AND c.city IN ({', '.join([f'{chr(39)}{c}{chr(39)}' for c in de_cities])})" if de_cities else ""
        df = run_query(f"""
            SELECT c.city, c.state, il.year AS `Year`,
                   il.median_household_income AS `Median Household Income ($)`
            FROM income_levels il JOIN cities c ON il.city_id = c.city_id
            WHERE il.year = {de_year}
            {city_clause}
            ORDER BY il.median_household_income DESC
            LIMIT 5000
        """)
        st.markdown(f"<p style='font-size:12px;color:#888580;font-family:\"Source Serif 4\",serif;'>{len(df):,} rows returned</p>", unsafe_allow_html=True)
        st.dataframe(df.rename(columns={"city": "City", "state": "State"}),
                     use_container_width=True, hide_index=True)

    elif table == "Mortgage Rates":
        df = run_query("""
            SELECT date AS `Date`,
                   mortgage_rate_30yr AS `30-Yr Fixed Rate (%)`
            FROM interest_rates
            ORDER BY date DESC
        """)
        st.markdown(f"<p style='font-size:12px;color:#888580;font-family:\"Source Serif 4\",serif;'>{len(df):,} weekly observations (FRED)</p>", unsafe_allow_html=True)
        fig = go.Figure(go.Scatter(
            x=df["Date"], y=df["30-Yr Fixed Rate (%)"],
            mode="lines", line=dict(color=C["primary"], width=2),
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>Rate: %{y:.2f}%<extra></extra>"
        ))
        fig = chart_layout(fig, "Figure 6.1 — 30-Year Fixed Mortgage Rate (FRED), 2015–2026",
                           xtitle="Date", ytitle="Rate (%)", height=340)
        fig.update_layout(yaxis=dict(ticksuffix="%"))
        st.plotly_chart(fig, use_container_width=True)
        caption("Figure 6.1", "Weekly average 30-year fixed mortgage rate from the Federal Reserve Economic Data (FRED). Used as the discount rate in all mortgage cost estimates throughout this platform.", source="Federal Reserve Economic Data (FRED)")
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif table == "Affordability Summary":
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            de_cities = st.multiselect("Filter by City", cities, key="de_as_cities")
        with f2:
            de_year = st.selectbox("Year", YEAR_OPTIONS, index=0, key="de_as_year")
        with f3:
            sort_by = st.selectbox("Sort By", ["Price-to-Income (desc)", "Rent Burden (desc)", "City (A-Z)"], key="de_sort")

        sort_map = {
            "Price-to-Income (desc)": "price_to_income_ratio DESC",
            "Rent Burden (desc)":     "rent_to_income_pct DESC",
            "City (A-Z)":             "c.city ASC",
        }
        city_clause = f"AND c.city IN ({', '.join([f'{chr(39)}{c}{chr(39)}' for c in de_cities])})" if de_cities else ""

        df = run_query(f"""
            SELECT c.city, c.state,
                   il.year                                                        AS `Year`,
                   ROUND(AVG(hp.median_home_value), 0)                            AS `Avg Home Value ($)`,
                   il.median_household_income                                     AS `Median Income ($)`,
                   ROUND(AVG(hp.median_home_value) / il.median_household_income, 2) AS price_to_income_ratio,
                   ROUND(AVG(rp.median_rent), 0)                                  AS `Avg Monthly Rent ($)`,
                   ROUND((AVG(rp.median_rent) * 12) / il.median_household_income * 100, 1) AS rent_to_income_pct
            FROM home_prices hp
            JOIN cities c ON hp.city_id = c.city_id
            JOIN income_levels il ON c.city_id = il.city_id AND YEAR(hp.date) = il.year
            LEFT JOIN rent_prices rp ON c.city_id = rp.city_id
                AND YEAR(rp.date) = il.year
            WHERE il.year = {de_year}
            {city_clause}
            GROUP BY c.city_id, c.city, c.state, il.year, il.median_household_income
            ORDER BY {sort_map[sort_by]}
            LIMIT 200
        """)

        df = df.rename(columns={
            "city": "City", "state": "State",
            "price_to_income_ratio": "Price-to-Income Ratio",
            "rent_to_income_pct": "Rent-to-Income (%)",
        })
        st.markdown(f"<p style='font-size:12px;color:#888580;font-family:\"Source Serif 4\",serif;'>{len(df):,} metros shown (max 200) — {de_year}</p>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"housing_affordability_summary_{de_year}.csv",
            mime="text/csv",
        )