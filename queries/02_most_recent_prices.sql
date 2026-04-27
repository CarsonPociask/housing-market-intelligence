-- --------------------------------------------------------
-- Query 02: Most Recent Home Price Per City
-- Purpose:  Retrieve the latest available home price for
--           all cities, ranked most expensive first.
-- Note:     Includes small resort markets (Jackson, WY etc.)
--           Consider filtering by metro size in dashboard.
-- --------------------------------------------------------

USE housing_intelligence;

SELECT 
    c.city,
    c.state,
    hp.date,
    hp.median_home_value
FROM home_prices hp
JOIN cities c ON hp.city_id = c.city_id
WHERE hp.date = (
    SELECT MAX(date) 
    FROM home_prices
)
ORDER BY hp.median_home_value DESC
LIMIT 20;