CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE CHECK (LENGTH(username) > 3),
    password TEXT NOT NULL CHECK (LENGTH(password) > 5),
    admin BOOLEAN DEFAULT false,
    visible INTEGER DEFAULT 1 NOT NULL
);

CREATE TABLE pictures (
    id SERIAL PRIMARY KEY,
    data BYTEA NOT NULL,
    visible INTEGER DEFAULT 1 NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    visible INTEGER DEFAULT 1 NOT NULL,
    outcome INTEGER NOT NULL,
    account_id INTEGER REFERENCES accounts NOT NULL,
    picture_id INTEGER REFERENCES pictures
);

CREATE TABLE budgets (
    id SERIAL PRIMARY KEY,
    period DATE NOT NULL,
    amount FLOAT DEFAULT 0 NOT NULL CHECK (amount >=0),
    category_id INTEGER REFERENCES categories NOT NULL
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100),
    amount FLOAT NOT NULL CHECK (amount >= 0),
    created_at TIMESTAMP NOT NULL,
    visible INTEGER DEFAULT 1 NOT NULL,
    picture_id INTEGER REFERENCES pictures,
    category_id INTEGER REFERENCES categories NOT NULL
);

CREATE TABLE subcategories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    visible INTEGER DEFAULT 1 NOT NULL,
    category_id INTEGER REFERENCES categories NOT NULL
);

