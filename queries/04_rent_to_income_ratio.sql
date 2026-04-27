-- --------------------------------------------------------
-- Query 04: Rent-to-Income Ratio with Burden Flag
-- Purpose:  Computes the percentage of median household
--           income consumed by median annual rent.
--           The 30% threshold is the standard definition
--           of rent burden used by HUD and economists.
-- Usage:    Change the year filter to compare across years.
-- --------------------------------------------------------

USE housing_intelligence;

SELECT 
    c.city,
    c.state,
    il.year,
    ROUND(AVG(rp.median_rent), 2)                                         AS avg_monthly_rent,
    il.median_household_income,
    ROUND((AVG(rp.median_rent) * 12) / il.median_household_income * 100, 2) AS rent_to_income_pct,
    CASE 
        WHEN (AVG(rp.median_rent) * 12) / il.median_household_income > 0.30 
        THEN 'Rent Burdened'
        ELSE 'Affordable'
    END AS burden_status
FROM rent_prices rp
JOIN cities c ON rp.city_id = c.city_id
JOIN income_levels il 
    ON c.city_id = il.city_id 
    AND YEAR(rp.date) = il.year
WHERE il.year = 2023
GROUP BY c.city_id, c.city, c.state, il.year, il.median_household_income
ORDER BY rent_to_income_pct DESC
LIMIT 20;