USE housing_intelligence;

CREATE TABLE income_levels (
    income_id                INT AUTO_INCREMENT PRIMARY KEY,
    city_id                  INT NOT NULL,
    year                     YEAR NOT NULL,
    median_household_income  DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    UNIQUE KEY unique_city_year (city_id, year)
);

SHOW COLUMNS FROM income_levels;