-- --------------------------------------------------------
-- Query 05: Year-Over-Year Home Price Growth by City
-- Purpose:  Uses the LAG() window function to compare each
--           city's average annual home value to the prior
--           year, returning a YoY growth percentage.
--           Sorted to surface the fastest appreciating
--           markets across all years in the dataset.
-- Concepts: Window functions, LAG(), subquery, PARTITION BY
-- --------------------------------------------------------

USE housing_intelligence;

SELECT 
    city,
    state,
    year,
    avg_home_value,
    prev_year_value,
    ROUND(
        (avg_home_value - prev_year_value) / prev_year_value * 100
    , 2) AS price_growth_yoy_pct
FROM (
    SELECT 
        c.city,
        c.state,
        YEAR(hp.date)                        AS year,
        ROUND(AVG(hp.median_home_value), 2)  AS avg_home_value,
        LAG(ROUND(AVG(hp.median_home_value), 2)) 
            OVER (
                PARTITION BY c.city_id 
                ORDER BY YEAR(hp.date)
            )                                AS prev_year_value
    FROM home_prices hp
    JOIN cities c ON hp.city_id = c.city_id
    GROUP BY c.city_id, c.city, c.state, YEAR(hp.date)
) AS yearly
WHERE prev_year_value IS NOT NULL
ORDER BY price_growth_yoy_pct DESC
LIMIT 20;