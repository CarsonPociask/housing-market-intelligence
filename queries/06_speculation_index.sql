-- --------------------------------------------------------
-- Query 06: Speculation Index by City and Year
-- Purpose:  Computes the divergence between home price
--           growth and income growth. A large positive
--           value signals prices rising faster than
--           economic fundamentals can support
-- Formula:  Speculation Index = Price Growth YoY% - Income Growth YoY%
-- Concepts: Two window function subqueries joined together,
--           LAG(), PARTITION BY, multi-table derived joins
-- --------------------------------------------------------

USE housing_intelligence;

SELECT 
    price_data.city,
    price_data.state,
    price_data.year,
    price_data.price_growth_yoy_pct,
    income_data.income_growth_yoy_pct,
    ROUND(
        price_data.price_growth_yoy_pct - income_data.income_growth_yoy_pct
    , 2) AS speculation_index
FROM (
    SELECT 
        c.city_id,
        c.city,
        c.state,
        YEAR(hp.date) AS year,
        ROUND(
            (AVG(hp.median_home_value) - LAG(AVG(hp.median_home_value)) 
                OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)))
            / LAG(AVG(hp.median_home_value)) 
                OVER (PARTITION BY c.city_id ORDER BY YEAR(hp.date)) * 100
        , 2) AS price_growth_yoy_pct
    FROM home_prices hp
    JOIN cities c ON hp.city_id = c.city_id
    GROUP BY c.city_id, c.city, c.state, YEAR(hp.date)
) AS price_data
JOIN (
    SELECT 
        city_id,
        year,
        ROUND(
            (median_household_income - LAG(median_household_income) 
                OVER (PARTITION BY city_id ORDER BY year))
            / LAG(median_household_income) 
                OVER (PARTITION BY city_id ORDER BY year) * 100
        , 2) AS income_growth_yoy_pct
    FROM income_levels
) AS income_data
    ON price_data.city_id = income_data.city_id
    AND price_data.year = income_data.year
WHERE price_data.price_growth_yoy_pct IS NOT NULL
  AND income_data.income_growth_yoy_pct IS NOT NULL
ORDER BY speculation_index DESC
LIMIT 20;