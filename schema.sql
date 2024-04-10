-- For now, creating tables into a dummydata database for testing purposes
-- This will be changed to a real database in the future

-- CREATE DATABASE IF NOT EXISTS dummydata; just in case we need to create the database

CREATE TABLE IF NOT EXISTS app_user(
    user_id     SERIAL,
    email       VARCHAR(255) NOT NULL     UNIQUE,
    username    VARCHAR(255) NOT NULL     UNIQUE,
    password    VARCHAR(255) NOT NULL,

    PRIMARY KEY(user_id)
);


