CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    admin BOOLEAN DEFAULT false,
    visible INTEGER DEFAULT 1,
    picture_id INTEGER REFERENCES pictures
);

CREATE TABLE outcome_budgets (
    id SERIAL PRIMARY KEY,
    period DATE NOT NULL,
    amount FLOAT NOT NULL,
    category_id INTEGER REFERENCES categories,
    account_id INTEGER REFERENCES accounts
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    visible INTEGER DEFAULT 1,
    outcome BOOLEAN
);

CREATE TABLE pictures (
    id SERIAL PRIMARY KEY,
    data BYTEA NOT NULL,
    visible INTEGER DEFAULT 1
);

CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    visible integer DEFAULT 1
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100),
    amount FLOAT NOT NULL,
    created_at TIMESTAMP,
    visible INTEGER DEFAULT 1 NOT NULL,
    account_id INTEGER REFERENCES accounts,
    picture_id INTEGER REFERENCES pictures,
    category_id INTEGER REFERENCES categories
);

CREATE TABLE categories_stores (
    store_id INTEGER REFERENCES stores,
    category_id INTEGER REFERENCES categories
);
