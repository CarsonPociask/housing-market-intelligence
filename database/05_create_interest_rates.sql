USE housing_intelligence;

CREATE TABLE interest_rates (
    rate_id              INT AUTO_INCREMENT PRIMARY KEY,
    date                 DATE NOT NULL,
    mortgage_rate_30yr   DECIMAL(5, 2) NOT NULL,
    UNIQUE KEY unique_date (date)
);

SHOW COLUMNS FROM interest_rates;
