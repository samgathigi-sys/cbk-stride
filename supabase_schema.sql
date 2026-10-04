-- ============================================================================
-- STRIDE(TM) AGM / EVENTS SCHEMA FOR SUPABASE (PostgreSQL)
-- Paste into Supabase: SQL Editor -> New query -> Run.
-- Safe to re-run: every statement uses IF NOT EXISTS.
-- ============================================================================

CREATE TABLE IF NOT EXISTS events_registry (
    id              BIGSERIAL PRIMARY KEY,
    event_id        TEXT UNIQUE NOT NULL,
    title           TEXT NOT NULL,
    organizer_name  TEXT NOT NULL,
    category        TEXT NOT NULL,
    event_date      TEXT NOT NULL,
    event_time      TEXT DEFAULT '09:00',
    venue           TEXT NOT NULL,
    description     TEXT DEFAULT '',
    gate_mode       TEXT DEFAULT 'DUAL_GATE',
    is_paid         INTEGER DEFAULT 1,
    standard_price  DOUBLE PRECISION DEFAULT 1000.0,
    vip_price       DOUBLE PRECISION DEFAULT 3500.0,
    mpesa_paybill   TEXT DEFAULT '849200',
    created_at      TEXT NOT NULL,
    status          TEXT DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS event_tickets_registry (
    id              BIGSERIAL PRIMARY KEY,
    ticket_id       TEXT UNIQUE NOT NULL,
    event_id        TEXT NOT NULL,
    attendee_name   TEXT NOT NULL,
    email           TEXT NOT NULL,
    phone           TEXT NOT NULL,
    organization    TEXT DEFAULT '',
    ticket_tier     TEXT NOT NULL,
    amount_paid     DOUBLE PRECISION DEFAULT 0.0,
    mpesa_trans_id  TEXT NOT NULL,
    gate_status     TEXT DEFAULT 'REGISTERED',
    checkin_time    TEXT DEFAULT '',
    created_at      TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tickets_event ON event_tickets_registry (event_id);

CREATE TABLE IF NOT EXISTS event_ballots_registry (
    id                  BIGSERIAL PRIMARY KEY,
    event_id            TEXT NOT NULL,
    ticket_id           TEXT NOT NULL,
    voter_name          TEXT NOT NULL,
    voter_organization  TEXT DEFAULT '',
    voting_weight       INTEGER DEFAULT 1,
    res1_vote           TEXT NOT NULL,
    res2_candidate      TEXT NOT NULL,
    res3_auditor        TEXT NOT NULL,
    ballot_hash         TEXT NOT NULL,
    cast_time           TEXT NOT NULL,
    UNIQUE (event_id, ticket_id)
);

CREATE TABLE IF NOT EXISTS event_feedback_registry (
    id              BIGSERIAL PRIMARY KEY,
    event_id        TEXT NOT NULL,
    ticket_id       TEXT DEFAULT '',
    attendee_name   TEXT NOT NULL,
    rating          INTEGER NOT NULL,
    feedback_text   TEXT NOT NULL,
    sentiment_score DOUBLE PRECISION NOT NULL,
    sentiment_label TEXT NOT NULL,
    aspects_json    TEXT DEFAULT '[]',
    submitted_at    TEXT NOT NULL
);

-- Ballot paper set by the Returning Officer (replaces st.session_state).
-- One row per event; config is stored as JSON text. locked = voting has opened.
CREATE TABLE IF NOT EXISTS event_ballot_config (
    event_id    TEXT PRIMARY KEY,
    config_json TEXT NOT NULL,
    locked      INTEGER DEFAULT 0,
    updated_at  TEXT NOT NULL
);

-- Supabase exposes tables over a public API by default. This app connects with a
-- direct database login, so turn on Row Level Security with no policies. That
-- blocks the public API from reading these tables while the app still works.
ALTER TABLE events_registry          ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_tickets_registry   ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_ballots_registry   ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_feedback_registry  ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_ballot_config      ENABLE ROW LEVEL SECURITY;
