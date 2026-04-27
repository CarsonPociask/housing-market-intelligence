-- --------------------------------------------------------
-- Query 03: Price-to-Income Ratio by City
-- Purpose:  Computes the ratio of average annual home price
--           to median household income for each city.
--           Values above 5x are generally considered
--           unaffordable. Values above 8x are severely
--           unaffordable.
-- Usage:    Change the year filter to compare across years.
-- --------------------------------------------------------

USE housing_intelligence;

SELECT 
    c.city,
    c.state,
    il.year,
    ROUND(AVG(hp.median_home_value), 2)   AS avg_home_value,
    il.median_household_income,
    ROUND(AVG(hp.median_home_value) / il.median_household_income, 2) AS price_to_income_ratio
FROM home_prices hp
JOIN cities c ON hp.city_id = c.city_id
JOIN income_levels il 
    ON c.city_id = il.city_id 
    AND YEAR(hp.date) = il.year
WHERE il.year = 2023
GROUP BY c.city_id, c.city, c.state, il.year, il.median_household_income
ORDER BY price_to_income_ratio DESC
LIMIT 20;