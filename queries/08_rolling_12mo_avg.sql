-- --------------------------------------------------------
-- Query 08: Rolling 12-Month Average Home Price
-- Purpose:  Smooths monthly price volatility by computing
--           a trailing 12-month average for each city.
--           Useful for identifying the underlying trend
--           without noise from seasonal fluctuations.
-- Usage:    Replace city filter to analyze any market.
-- Concepts: AVG() OVER window function, ROWS BETWEEN,
--           PARTITION BY, sliding window aggregation
-- --------------------------------------------------------

SELECT
    c.city,
    c.state,
    hp.date,
    hp.median_home_value,
    ROUND(
        AVG(hp.median_home_value) OVER (
            PARTITION BY c.city_id
            ORDER BY hp.date
            ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
        )
    , 2) AS rolling_12mo_avg
FROM home_prices hp
JOIN cities c ON hp.city_id = c.city_id
WHERE c.city = 'Austin, TX'
  AND c.state = 'TX'
ORDER BY hp.date ASC;