-- --------------------------------------------------------
-- Query 07: Rent vs. Buy Comparison by City
-- Purpose:  Compares median monthly rent to estimated
--           monthly mortgage cost using actual FRED rates.
--           Mortgage assumes 20% down, 30-yr fixed.
--           Ratio > 1 = renting is cheaper monthly.
--           Ratio < 1 = buying is cheaper monthly.
-- Note:     Does not account for equity building, taxes,
--           maintenance, or appreciation — pure monthly
--           cash flow comparison only.
-- Concepts: Four table join, amortization formula,
--           POWER(), CASE WHEN, MONTH() date matching
-- --------------------------------------------------------

SELECT 
    c.city,
    c.state,
    YEAR(rp.date)                         AS year,
    ROUND(AVG(rp.median_rent), 2)         AS avg_monthly_rent,
    ROUND(AVG(hp.median_home_value), 2)   AS avg_home_value,
    ROUND(AVG(ir.mortgage_rate_30yr), 4)  AS avg_mortgage_rate,
    ROUND(
        (AVG(hp.median_home_value) * 0.80) * 
        (AVG(ir.mortgage_rate_30yr) / 100 / 12) /
        (1 - POWER(1 + AVG(ir.mortgage_rate_30yr) / 100 / 12, -360))
    , 2)                                  AS est_monthly_mortgage,
    ROUND(
        AVG(rp.median_rent) /
        (
            (AVG(hp.median_home_value) * 0.80) *
            (AVG(ir.mortgage_rate_30yr) / 100 / 12) /
            (1 - POWER(1 + AVG(ir.mortgage_rate_30yr) / 100 / 12, -360))
        )
    , 2)                                  AS rent_vs_buy_ratio,
    CASE
        WHEN AVG(rp.median_rent) /
            (
                (AVG(hp.median_home_value) * 0.80) *
                (AVG(ir.mortgage_rate_30yr) / 100 / 12) /
                (1 - POWER(1 + AVG(ir.mortgage_rate_30yr) / 100 / 12, -360))
            ) > 1
        THEN 'Rent Favored'
        ELSE 'Buy Favored'
    END                                   AS recommendation
FROM rent_prices rp
JOIN cities c ON rp.city_id = c.city_id
JOIN home_prices hp 
    ON c.city_id = hp.city_id 
    AND YEAR(rp.date) = YEAR(hp.date)
    AND MONTH(rp.date) = MONTH(hp.date)
JOIN interest_rates ir 
    ON YEAR(rp.date) = YEAR(ir.date)
    AND MONTH(rp.date) = MONTH(ir.date)
WHERE YEAR(rp.date) = 2023
GROUP BY c.city_id, c.city, c.state, YEAR(rp.date)
ORDER BY rent_vs_buy_ratio ASC
LIMIT 20;