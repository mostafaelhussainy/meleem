CREATE TABLE categories (
    id UUID PRIMARY KEY, 
    name TEXT UNIQUE, 
    type category_type NOT NULL
);