-- --------------------------------------------------------
-- Query 10: Market Summary Ranking (Composite Score)
-- Purpose:  Combines price-to-income ratio, rent burden,
--           and price growth into a single market stress
--           score per city for a given year.
-- Weights:  Price-to-income  50%
--           Rent-to-income   30% (normalized to 0-10 scale)
--           Price growth YoY 20%
-- Thresholds: > 7 = High Stress
--             > 4 = Moderate Stress
--             <= 4 = Affordable
-- Note:     Score reflects conditions in the selected year.
--           Correcting markets may score lower than their
--           absolute price level suggests.
-- Concepts: CTEs (WITH clauses), composite scoring,
--           multi-CTE joins, CASE WHEN classification
-- --------------------------------------------------------

WITH affordability AS (
    SELECT
        c.city_id,
        c.city,
        c.state,
        ROUND(AVG(hp.median_home_value) / il.median_household_income, 2) AS price_to_income_ratio
    FROM home_prices hp
    JOIN cities c ON hp.city_id = c.city_id
    JOIN income_levels il
        ON c.city_id = il.city_id
        AND YEAR(hp.date) = il.year
    WHERE il.year = 2023
    GROUP BY c.city_id, c.city, c.state, il.median_household_income
),
rent_burden AS (
    SELECT
        c.city_id,
        ROUND((AVG(rp.median_rent) * 12) / il.median_household_income * 100, 2) AS rent_to_income_pct
    FROM rent_prices rp
    JOIN cities c ON rp.city_id = c.city_id
    JOIN income_levels il
        ON c.city_id = il.city_id
        AND YEAR(rp.date) = il.year
    WHERE il.year = 2023
    GROUP BY c.city_id, il.median_household_income
),
price_growth AS (
    SELECT
        city_id,
        city,
        price_growth_yoy_pct
    FROM (
        SELECT
            c.city_id,
            c.city,
            YEAR(hp.date) AS year,
            ROUND(
                (AVG(hp.median_home_value) - LAG(AVG(hp.median_home_value))
                    OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)))
                / LAG(AVG(hp.median_home_value))
                    OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)) * 100
            , 2) AS price_growth_yoy_pct
        FROM home_prices hp
        JOIN cities c ON hp.city_id = c.city_id
        GROUP BY c.city_id, c.city, YEAR(hp.date)
    ) AS growth
    WHERE year = 2023
)
SELECT
    a.city,
    a.state,
    a.price_to_income_ratio,
    rb.rent_to_income_pct,
    pg.price_growth_yoy_pct,
   ROUND(
    (a.price_to_income_ratio * 0.5) +
    (rb.rent_to_income_pct / 10 * 0.3) +
    (pg.price_growth_yoy_pct * 0.2)
, 2) AS market_stress_score,
CASE
    WHEN (a.price_to_income_ratio * 0.5) +
         (rb.rent_to_income_pct / 10 * 0.3) +
         (pg.price_growth_yoy_pct * 0.2) > 7
    THEN 'High Stress'
    WHEN (a.price_to_income_ratio * 0.5) +
         (rb.rent_to_income_pct / 10 * 0.3) +
         (pg.price_growth_yoy_pct * 0.2) > 4
    THEN 'Moderate Stress'
    ELSE 'Affordable'
END AS market_status
FROM affordability a
JOIN rent_burden rb ON a.city_id = rb.city_id
JOIN price_growth pg ON a.city_id = pg.city_id
ORDER BY market_stress_score ASC
LIMIT 20;