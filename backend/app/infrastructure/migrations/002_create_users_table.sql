CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password BYTEA NOT NULL,
    goal DECIMAL(18,4) DEFAULT 0 NOT NULL,
    savings DECIMAL(18,4) DEFAULT 0 NOT NULL,
    balance DECIMAL(18,4) DEFAULT 0 NOT NULL,
    currency_code CHAR(3) REFERENCES currencies(iso_code)
);