--liquibase formatted sql

--changeset dkothari:1

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS account_user (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_on TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    country_code VARCHAR(10),
    phone VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT true,
    last_logged_in TIMESTAMPTZ NOT NULL DEFAULT '1970-01-01 00:00:00+00',
    updated_on TIMESTAMPTZ NOT NULL DEFAULT current_timestamp
);

-- Indexes
CREATE INDEX IF NOT EXISTS ix_account_user_id ON account_user(id);
CREATE INDEX IF NOT EXISTS ix_account_user_email ON account_user(email);
CREATE INDEX IF NOT EXISTS ix_account_user_username ON account_user(username);
CREATE INDEX IF NOT EXISTS ix_accountuser_is_active ON account_user(is_active);
