--liquibase formatted sql

--changeset dkothari:2

-- Enable pgcrypto extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create tenant table
CREATE TABLE IF NOT EXISTS tenant (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_on TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    name VARCHAR(255) NOT NULL,
    host VARCHAR(255) NOT NULL UNIQUE,
    schema VARCHAR(64) NOT NULL UNIQUE,
    owner_id UUID NOT NULL REFERENCES account_user(id) ON DELETE CASCADE,
    is_active BOOLEAN NOT NULL DEFAULT true,
    updated_on TIMESTAMPTZ NOT NULL DEFAULT current_timestamp
);

-- Indexes
CREATE INDEX IF NOT EXISTS ix_tenant_id ON tenant(id);
CREATE INDEX IF NOT EXISTS ix_tenant_owner_id ON tenant(owner_id);
CREATE INDEX IF NOT EXISTS ix_tenant_owner_is_active ON tenant(owner_id, is_active);
