CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    amount DECIMAL(18,4) NOT NULL,
    currency_id CHAR(3) REFERENCES currencies(iso_code) NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    category_id UUID REFERENCES categories(id) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

