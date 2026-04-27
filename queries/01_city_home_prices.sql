-- --------------------------------------------------------
-- Query 01: Home Price History by City
-- Purpose:  Retrieve the full monthly home price history
--           for a specific city, ordered chronologically.
-- Usage:    Replace 'Austin, TX' and 'TX' with any city
--           in the database.
-- --------------------------------------------------------

USE housing_intelligence;

SELECT 
    c.city,
    c.state,
    hp.date,
    hp.median_home_value
FROM home_prices hp
JOIN cities c ON hp.city_id = c.city_id
WHERE c.city = 'Austin, TX'
  AND c.state = 'TX'
ORDER BY hp.date ASC;