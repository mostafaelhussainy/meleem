CREATE TABLE recurring_transaction_history (
    id UUID PRIMARY KEY,
    recurring_transaction_id UUID REFERENCES recurring_transactions(id),
    triggered_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);