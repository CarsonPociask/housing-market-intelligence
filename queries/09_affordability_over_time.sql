-- --------------------------------------------------------
-- Query 09: Affordability Change Over Time by City
-- Purpose:  Tracks how each city's price-to-income ratio
--           has shifted year over year. A positive
--           affordability_change means the city got less
--           affordable that year. Useful for identifying
--           cities in sustained deterioration vs. recovery.
-- Usage:    Replace city list with any cities of interest.
-- Concepts: LAG() window function on derived ratios,
--           nested subquery, multi-city comparison
-- --------------------------------------------------------

SELECT
    city,
    state,
    year,
    price_to_income_ratio,
    LAG(price_to_income_ratio) OVER (
        PARTITION BY city
        ORDER BY year
    ) AS prior_year_ratio,
    ROUND(
        price_to_income_ratio - LAG(price_to_income_ratio) OVER (
            PARTITION BY city
            ORDER BY year
        )
    , 2) AS affordability_change
FROM (
    SELECT
        c.city,
        c.state,
        il.year,
        ROUND(
            AVG(hp.median_home_value) / il.median_household_income
        , 2) AS price_to_income_ratio
    FROM home_prices hp
    JOIN cities c ON hp.city_id = c.city_id
    JOIN income_levels il
        ON c.city_id = il.city_id
        AND YEAR(hp.date) = il.year
    GROUP BY c.city_id, c.city, c.state, il.year, il.median_household_income
) AS ratios
WHERE city IN ('Austin, TX', 'Miami, FL', 'Minneapolis, MN', 'Boise City, ID', 'Chicago, IL')
ORDER BY city, year;