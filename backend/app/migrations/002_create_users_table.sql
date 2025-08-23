CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    goal DECIMAL(18,4),
    goal_currency_code CHAR(3) REFERENCES currencies(iso_code)
);