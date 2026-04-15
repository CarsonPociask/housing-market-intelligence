USE housing_intelligence;

CREATE TABLE rent_prices (
    rent_id      INT AUTO_INCREMENT PRIMARY KEY,
    city_id      INT NOT NULL,
    date         DATE NOT NULL,
    median_rent  DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    UNIQUE KEY unique_city_date (city_id, date)
);

SHOW COLUMNS FROM rent_prices;