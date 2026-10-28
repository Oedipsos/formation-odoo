-- =============================================================================
-- Mythical Creature Refuge — schema.sql (exercise 3.1)
-- PostgreSQL 14+. Re-runnable: drops everything, then recreates in dependency order.
--   psql -h localhost -U refuge -d refuge -f sql/schema.sql
-- Species list = state at chapter 3 (5 species). Kraken arrives with
-- migration 001 in exercise 6.5, which replaces chk_creatures_species.
-- =============================================================================

DROP TABLE IF EXISTS health_records CASCADE;
DROP TABLE IF EXISTS missions       CASCADE;
DROP TABLE IF EXISTS destinations   CASCADE;
DROP TABLE IF EXISTS employees      CASCADE;
DROP TABLE IF EXISTS creatures      CASCADE;
DROP TABLE IF EXISTS enclosures     CASCADE;

-- -----------------------------------------------------------------------------
-- enclosures: where creatures live
-- -----------------------------------------------------------------------------
CREATE TABLE enclosures (
    id        SERIAL       PRIMARY KEY,
    name      VARCHAR(100) NOT NULL UNIQUE,
    capacity  INTEGER      NOT NULL,
    CONSTRAINT chk_enclosures_capacity CHECK (capacity > 0)
);

-- -----------------------------------------------------------------------------
-- creatures: single-table storage for the whole Creature hierarchy
-- (species-specific columns are nullable or defaulted)
-- -----------------------------------------------------------------------------
CREATE TABLE creatures (
    id                  SERIAL       PRIMARY KEY,
    name                VARCHAR(100) NOT NULL UNIQUE,
    species             VARCHAR(20)  NOT NULL,
    origin              TEXT         NOT NULL,
    power_level         INTEGER      NOT NULL,
    element             VARCHAR(20),                       -- dragons only
    resurrection_count  INTEGER      NOT NULL DEFAULT 0,   -- meaningful for phoenixes
    in_refuge           BOOLEAN      NOT NULL DEFAULT TRUE,
    enclosure_id        INTEGER      REFERENCES enclosures (id) ON DELETE SET NULL,
    registered_at       TIMESTAMP    NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_creatures_species
        CHECK (species IN ('Dragon', 'Phoenix', 'Unicorn', 'Griffin', 'Basilisk')),
    CONSTRAINT chk_creatures_power_level
        CHECK (power_level BETWEEN 0 AND 100),
    CONSTRAINT chk_creatures_resurrection_count
        CHECK (resurrection_count >= 0),
    -- table-level check: the rule spans two columns
    CONSTRAINT chk_element_only_dragon
        CHECK (species = 'Dragon' OR element IS NULL)
);

-- -----------------------------------------------------------------------------
-- employees: single-table storage for Handler / Veterinarian
-- -----------------------------------------------------------------------------
CREATE TABLE employees (
    id                   SERIAL       PRIMARY KEY,
    full_name            VARCHAR(100) NOT NULL UNIQUE,   -- simplification, see 3.1 Q3
    email                VARCHAR(255) NOT NULL UNIQUE,
    role                 VARCHAR(20)  NOT NULL,
    certification_level  INTEGER,
    supervisor_id        INTEGER      REFERENCES employees (id) ON DELETE SET NULL,
    hired_on             DATE         NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT chk_employees_role
        CHECK (role IN ('handler', 'veterinarian')),
    CONSTRAINT chk_employees_certification_level
        CHECK (certification_level BETWEEN 1 AND 5),
    -- table-level check: handlers must be certified
    CONSTRAINT chk_handler_certified
        CHECK (role <> 'handler' OR certification_level IS NOT NULL)
);

-- -----------------------------------------------------------------------------
-- destinations: where missions go, with their danger multiplier
-- -----------------------------------------------------------------------------
CREATE TABLE destinations (
    id                 SERIAL       PRIMARY KEY,
    name               VARCHAR(100) NOT NULL UNIQUE,
    danger_multiplier  NUMERIC(3,1) NOT NULL DEFAULT 1.0,
    CONSTRAINT chk_destinations_danger_multiplier CHECK (danger_multiplier >= 1.0)
);

-- -----------------------------------------------------------------------------
-- missions: enriched junction table (creature x handler x destination)
-- -----------------------------------------------------------------------------
CREATE TABLE missions (
    id              SERIAL        PRIMARY KEY,
    creature_id     INTEGER       REFERENCES creatures (id)    ON DELETE RESTRICT,
    handler_id      INTEGER       REFERENCES employees (id)    ON DELETE RESTRICT,
    destination_id  INTEGER       REFERENCES destinations (id) ON DELETE RESTRICT,
    departure_date  DATE          NOT NULL,
    duration_days   INTEGER       NOT NULL,
    base_reward     NUMERIC(10,2) NOT NULL,
    returned_on     DATE,                                  -- NULL while ongoing
    notes           TEXT          NOT NULL DEFAULT '',

    CONSTRAINT chk_missions_duration_days     CHECK (duration_days > 0),
    CONSTRAINT chk_missions_base_reward       CHECK (base_reward >= 0),
    CONSTRAINT chk_return_after_departure     CHECK (returned_on >= departure_date),
    CONSTRAINT uq_creature_departure          UNIQUE (creature_id, departure_date)
);

-- -----------------------------------------------------------------------------
-- health_records: enriched junction table (creature x veterinarian)
-- -----------------------------------------------------------------------------
CREATE TABLE health_records (
    id           SERIAL         PRIMARY KEY,
    creature_id  INTEGER        REFERENCES creatures (id) ON DELETE CASCADE,
    vet_id       INTEGER        REFERENCES employees (id) ON DELETE RESTRICT,
    examined_on  DATE           NOT NULL DEFAULT CURRENT_DATE,
    status       VARCHAR(20)    NOT NULL,
    diagnosis    TEXT           NOT NULL,
    treatment    TEXT           NOT NULL DEFAULT '',

    CONSTRAINT chk_health_records_status
        CHECK (status IN ('healthy', 'under_observation', 'in_treatment', 'quarantine'))
);
