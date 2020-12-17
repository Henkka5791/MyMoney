CREATE TABLE accounts (
    id integer NOT NULL,
    username varchar(20) NOT NULL UNIQUE,
    password text NOT NULL,
    admin boolean DEFAULT false,
    visible integer DEFAULT 1,
    picture_id integer
);

CREATE TABLE outcome_budgets (
    id integer NOT NULL,
    period date NOT NULL,
    amount float NOT NULL,
    category_id integer,
    account_id integer
);

CREATE TABLE categories (
    id integer NOT NULL,
    name varchar(50) NOT NULL,
    visible integer DEFAULT 1,
    outcome boolean
);

CREATE TABLE pictures (
    id integer NOT NULL,
    data bytea NOT NULL,
    visible integer DEFAULT 1
);

CREATE TABLE stores (
    id integer NOT NULL,
    name varchar(50) NOT NULL,
    visible integer DEFAULT 1
);

CREATE TABLE transactions (
    id integer NOT NULL,
    description varchar(100),
    amount double precision NOT NULL,
    created_at timestamp without time zone,
    visible integer DEFAULT 1 NOT NULL,
    account_id integer,
    picture_id integer,
    category_id integer
);
