USE housing_intelligence;
-- All calculated metrics

CREATE TABLE affordability_metrics (
    metric_id                INT AUTO_INCREMENT PRIMARY KEY,
    city_id                  INT NOT NULL,
    year                     YEAR NOT NULL,
    price_to_income_ratio    DECIMAL(8, 2),
    rent_to_income_ratio     DECIMAL(8, 2),
    est_monthly_mortgage     DECIMAL(10, 2),
    rent_vs_buy_ratio        DECIMAL(8, 2),
    price_growth_yoy         DECIMAL(8, 4),
    income_growth_yoy        DECIMAL(8, 4),
    speculation_index        DECIMAL(8, 4),
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    UNIQUE KEY unique_city_year (city_id, year)
);

SHOW COLUMNS FROM affordability_metrics;