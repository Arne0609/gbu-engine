-- ============================================================================
-- GBU APP 4.0 – Datenmodell der Bewertungsengine (PostgreSQL DDL)
-- ============================================================================
--
-- Greenfield-Schema für die engine-getrennte GBU-/Cyber-Beurteilung.
-- Leitidee: FRAGEBOGEN und BEWERTUNGSENGINE sind vollständig getrennt.
--   * Eine Frage kann mehrere Gefährdungen beeinflussen (m:n).
--   * Eine Gefährdung wird aus mehreren Fragen bestimmt (Rollen + Regeln).
--   * Es wird NIE eine Bewertung direkt an einer Frage gespeichert.
--
-- Kernfehler der untersuchten Original-App, die hier STRUKTURELL vermieden
-- werden:
--   1. Fehlende Antwort wurde als „Kein Risiko" gewertet
--      -> eigener Zustand INCOMPLETE, siehe risk_status.
--   2. Fehlende Pflichtantwort ließ eine Gefährdung ganz verschwinden
--      -> rule_required_questions + Auswertungsreihenfolge (siehe Doku).
--   3. UI-Kategorie war mit der Bewertungsstruktur vermischt
--      -> question_categories ist reine Erhebungs-/Anzeigestruktur.
--
-- Konventionen:
--   * Primärschlüssel: UUID (gen_random_uuid(), benötigt pgcrypto).
--   * Zeitstempel: timestamptz, UTC.
--   * Fachliche, stabile Codes (M032, MC4, f033, 8.1) stehen in *_code /
--     legacy_id-Spalten, NICHT im Primärschlüssel.
--   * Kontrollierte Ausdruckssprache der Regeln: JSONB (siehe
--     rule_engine.schema.json). Kein frei ausführbarer Code.
--
-- Reihenfolge der Statements ist so gewählt, dass FKs immer auf bereits
-- angelegte Tabellen zeigen. DROP-Reihenfolge ist umgekehrt (am Dateiende
-- als Kommentar dokumentiert).
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- gen_random_uuid()

-- ----------------------------------------------------------------------------
-- 0. ENUM-Typen (fachliche Wertelisten)
-- ----------------------------------------------------------------------------
-- Neue Werte dürfen später NUR angehängt werden (ALTER TYPE ... ADD VALUE),
-- bestehende nie umbenannt/entfernt werden – sie stecken in gespeicherten
-- Daten und in abgeschlossenen, revisionssicheren Berichten.

CREATE TYPE domain_type          AS ENUM ('GBU', 'CYBER', 'BOTH');

CREATE TYPE lift_type            AS ENUM ('TRACTION', 'HYDRAULIC', 'ROPE_HYDRAULIC',
                                         'PLATFORM', 'OTHER');

CREATE TYPE drive_type           AS ENUM ('GEARED', 'GEARLESS', 'HYDRAULIC',
                                         'SPINDLE', 'CHAIN', 'RACK_PINION', 'OTHER');

CREATE TYPE usage_type           AS ENUM ('PUBLIC', 'SEMI_PUBLIC', 'INSTRUCTED_ONLY',
                                         'PRIVATE', 'WORKPLACE', 'OTHER');

CREATE TYPE assessment_type      AS ENUM ('GBU', 'CYBER', 'GBU_CYBER');

CREATE TYPE assessment_status    AS ENUM ('DRAFT', 'IN_PROGRESS', 'READY_FOR_REVIEW',
                                         'COMPLETED', 'LOCKED', 'ARCHIVED');

CREATE TYPE question_type        AS ENUM ('YES_NO', 'YES_NO_NA', 'SELECT', 'MULTI_SELECT',
                                         'NUMBER', 'TEXT', 'DATE', 'PHOTO',
                                         'TEXT_PHOTO', 'SELECT_PHOTO');

CREATE TYPE visibility_effect    AS ENUM ('SHOW', 'HIDE', 'REQUIRE');

-- Rolle einer Frage FÜR eine Gefährdung (m:n). Bestimmt, wie die Antwort in
-- die Auswertung eingeht – nicht, wo die Frage im Fragebogen steht.
-- 'REQUIRED' ist BEWUSST keine Rolle mehr: Pflicht-Sein ist eine eigene
-- Dimension (required_mode), weil dieselbe Frage in einer Gefährdung Pflicht
-- und in einer anderen optional sein kann (Delta 4: M087 bewertet trotz leerer
-- Ortsfragen, MC4–MC9 nicht).
CREATE TYPE hazard_question_role AS ENUM ('APPLICABILITY', 'TRIGGER', 'COMPENSATION',
                                         'MODIFIER', 'ACCESS_FACTOR',
                                         'OPTIONAL', 'DOCUMENTATION');

-- Ob eine Frage FÜR EINE GEFÄHRDUNG beantwortet sein muss, damit diese
-- bewertet wird. Gefährdungsspezifisch (nicht global, nicht pro Regel).
CREATE TYPE required_mode        AS ENUM ('NEVER', 'ALWAYS', 'CONDITIONAL');

-- Auswertungsmodus einer Gefährdung bei fehlenden Antworten.
--   STANDARD         : Regellogik entscheidet.
--   PARTIAL_ALLOWED  : Teilantworten genügen (Ortsblöcke, ANY) – leere
--                      Nicht-Pflichtfragen blockieren die Bewertung nicht.
--   STRICT_REQUIRED  : jede ALWAYS-Pflichtfrage muss beantwortet sein, sonst
--                      INCOMPLETE (Cyber-Bauplan MC4–MC9).
CREATE TYPE evaluation_mode      AS ENUM ('STANDARD', 'PARTIAL_ALLOWED',
                                         'STRICT_REQUIRED');

-- Sechs echte Bewertungszustände (statt der vier der Original-App).
CREATE TYPE risk_status          AS ENUM ('INCOMPLETE', 'NOT_APPLICABLE', 'NO_RISK',
                                         'LOW', 'MEDIUM', 'HIGH');

CREATE TYPE aggregation_type     AS ENUM ('NONE', 'ANY', 'ALL', 'MAXIMUM', 'MINIMUM',
                                         'DECISION_TABLE');

-- Herkunft einer Regel – trennt rekonstruierte Original-Logik von eigener
-- fachlicher Logik (die zwei Regelwelten aus dem Konzept).
CREATE TYPE rule_origin          AS ENUM ('RECONSTRUCTED_ORIGINAL', 'NORM_DERIVED',
                                         'OWN_RULE');

-- Belegtiefe – wie gut das ORIGINAL-Verhalten beobachtet ist (aus dem
-- Reverse-Engineering, nur intern/Admin).
CREATE TYPE evidence_level       AS ENUM ('DIRECT', 'HIGH_CONFIDENCE', 'INFERRED',
                                         'HYPOTHESIS');

-- Unsere fachliche Haltung zur Regel – getrennt von der Belegtiefe.
--   VERIFIED        : fachlich geprüft, so gewollt.
--   REVIEW_REQUIRED : rekonstruiert, aber fachlich zu prüfen/abzuweichen
--                     (z. B. M032-Notruflogik).
--   KNOWN_BUG       : bewusst NICHT übernommenes Fehlverhalten des Originals
--                     (PARTIAL_EVALUATION_BUG) – nur zur Dokumentation.
--   NOT_IMPLEMENTED : Gefährdung ohne auslösbare Fragen (z. B. MC13).
CREATE TYPE quality_status       AS ENUM ('VERIFIED', 'REVIEW_REQUIRED',
                                         'KNOWN_BUG', 'NOT_IMPLEMENTED');

CREATE TYPE measure_type         AS ENUM ('TECHNICAL', 'ORGANISATIONAL', 'INSPECTION',
                                         'DOCUMENTATION', 'REPAIR', 'REPLACEMENT',
                                         'WARNING', 'OTHER');

CREATE TYPE measure_relation     AS ENUM ('AND', 'OR', 'SINGLE');

CREATE TYPE source_type          AS ENUM ('TRBS', 'DIN', 'EN', 'EU_DIRECTIVE',
                                         'EU_REGULATION', 'LAW', 'DGUV', 'OTHER');

CREATE TYPE rule_version_status  AS ENUM ('DRAFT', 'PUBLISHED', 'ARCHIVED');

CREATE TYPE audit_action         AS ENUM ('CREATE', 'UPDATE', 'DELETE', 'ANSWER',
                                         'OVERRIDE', 'COMPLETE', 'REOPEN', 'PUBLISH',
                                         'LOCK', 'ARCHIVE');

-- ----------------------------------------------------------------------------
-- 1. Mandant / Organisation / Benutzer
-- ----------------------------------------------------------------------------

CREATE TABLE tenants (
    id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name         varchar(200) NOT NULL,
    slug         varchar(80)  NOT NULL UNIQUE,
    active       boolean      NOT NULL DEFAULT true,
    created_at   timestamptz  NOT NULL DEFAULT now(),
    updated_at   timestamptz  NOT NULL DEFAULT now()
);

CREATE TABLE users (
    id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id    uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    username     varchar(120) NOT NULL,
    display_name varchar(200) NOT NULL,
    email        varchar(320),
    role         varchar(40)  NOT NULL DEFAULT 'ASSESSOR',   -- ASSESSOR/ADMIN/APPRENTICE/…
    active       boolean      NOT NULL DEFAULT true,
    created_at   timestamptz  NOT NULL DEFAULT now(),
    updated_at   timestamptz  NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, username)
);
CREATE INDEX idx_users_tenant ON users(tenant_id);

-- ----------------------------------------------------------------------------
-- 2. Anlagen (Assets)
-- ----------------------------------------------------------------------------
-- Anlagendaten dienen zugleich als Applicability-Filter (welche Gefährdungen
-- für diese Bauart überhaupt relevant sind).

CREATE TABLE assets (
    id                    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id             uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    asset_number          varchar(80),          -- interne Anlagennummer
    external_asset_number varchar(80),          -- z. B. Auftrag/Fremdsystem
    address_street        varchar(200),
    address_zip           varchar(20),
    address_city          varchar(120),
    address_country       varchar(80) DEFAULT 'DE',
    manufacturer          varchar(160),
    year_of_construction  integer CHECK (year_of_construction BETWEEN 1850 AND 2100),
    commissioning_date    date,
    lift_type             lift_type,
    drive_type            drive_type,
    rated_load_kg         integer CHECK (rated_load_kg >= 0),
    rated_speed_ms        numeric(5,2) CHECK (rated_speed_ms >= 0),
    stops                 integer CHECK (stops >= 0),
    usage_type            usage_type,
    accessibility_usage   boolean,              -- Barrierefreiheit / eingeschr. Mobilität
    norm_at_placement     varchar(120),         -- Norm bei Inverkehrbringen
    modernizations        text,
    serial_number         varchar(120),
    notes                 text,
    created_at            timestamptz NOT NULL DEFAULT now(),
    updated_at            timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_assets_tenant ON assets(tenant_id);
CREATE INDEX idx_assets_number ON assets(tenant_id, asset_number);

-- ----------------------------------------------------------------------------
-- 3. Regelversionen (bevor assessments, da FK)
-- ----------------------------------------------------------------------------
-- Eine abgeschlossene GBU bleibt für immer an ihrer Regelversion hängen –
-- ein späteres Update ändert nie rückwirkend alte Berichte.

CREATE TABLE rule_versions (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name          varchar(160) NOT NULL,          -- „GBU-Regelwerk"
    version       varchar(40)  NOT NULL,          -- „2026.1"
    domain        domain_type  NOT NULL DEFAULT 'BOTH',
    valid_from    date         NOT NULL,
    valid_to      date,                           -- NULL = aktuell gültig
    status        rule_version_status NOT NULL DEFAULT 'DRAFT',
    description    text,
    created_by     uuid REFERENCES users(id),
    created_at     timestamptz NOT NULL DEFAULT now(),
    published_at   timestamptz,
    UNIQUE (name, version),
    CHECK (valid_to IS NULL OR valid_to >= valid_from)
);

-- ----------------------------------------------------------------------------
-- 4. Beurteilungen (Assessments)
-- ----------------------------------------------------------------------------

CREATE TABLE assessments (
    id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id         uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    asset_id          uuid NOT NULL REFERENCES assets(id) ON DELETE RESTRICT,
    assessment_number varchar(60),               -- z. B. GBU-2026-000123
    type              assessment_type NOT NULL DEFAULT 'GBU',
    status            assessment_status NOT NULL DEFAULT 'DRAFT',
    rule_version_id   uuid NOT NULL REFERENCES rule_versions(id) ON DELETE RESTRICT,
    assessor_user_id  uuid REFERENCES users(id),
    started_at        timestamptz,
    completed_at      timestamptz,
    locked_at         timestamptz,
    created_at        timestamptz NOT NULL DEFAULT now(),
    updated_at        timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_assessments_tenant ON assessments(tenant_id);
CREATE INDEX idx_assessments_asset  ON assessments(asset_id);
CREATE INDEX idx_assessments_status ON assessments(tenant_id, status);

-- ----------------------------------------------------------------------------
-- 5. Fragebogen: Kategorien (reine UI-/Erhebungsstruktur)
-- ----------------------------------------------------------------------------
-- WICHTIG: Kategorie erzwingt KEINE Abhängigkeit zur Gefährdungsstruktur.
-- Eine Frage unter „Schacht" darf M035, M060, M081 beeinflussen.

CREATE TABLE question_categories (
    id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    domain     domain_type NOT NULL DEFAULT 'GBU',
    code       varchar(20) NOT NULL,             -- „08", „12"
    title      varchar(200) NOT NULL,
    sort_order integer NOT NULL DEFAULT 0,
    active     boolean NOT NULL DEFAULT true,
    UNIQUE (code)
);

-- ----------------------------------------------------------------------------
-- 6. Fragen
-- ----------------------------------------------------------------------------

CREATE TABLE questions (
    id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    legacy_id        varchar(40),                -- „f033" (nur Mapping, nicht tragend)
    ui_number        varchar(20),                -- „8.1"
    category_id      uuid REFERENCES question_categories(id) ON DELETE SET NULL,
    domain           domain_type NOT NULL DEFAULT 'GBU',
    code             varchar(80) NOT NULL UNIQUE,-- stabile, sprechende ID: q_emergency_call_present
    text             text NOT NULL,
    question_type    question_type NOT NULL,
    required_default boolean NOT NULL DEFAULT false,
    help_text        text,
    help_media_id    uuid,                       -- optionale Grafik (Media-Store extern)
    active           boolean NOT NULL DEFAULT true,
    active_from      varchar(40),                -- Regelversion, ab der die Frage gilt
    active_to        varchar(40),
    sort_order       integer NOT NULL DEFAULT 0,
    created_at       timestamptz NOT NULL DEFAULT now(),
    updated_at       timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_questions_category ON questions(category_id);
CREATE INDEX idx_questions_legacy   ON questions(legacy_id);
CREATE INDEX idx_questions_domain   ON questions(domain);

-- ----------------------------------------------------------------------------
-- 7. Antwortoptionen (Dropdownwerte als eigene Datensätze)
-- ----------------------------------------------------------------------------
-- Bewertung hängt am semantischen value, nie am Anzeigetext.

CREATE TABLE question_options (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id    uuid NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    value          varchar(80) NOT NULL,         -- KEY_SAFE
    label          varchar(300) NOT NULL,        -- „Ja, über Schlüsseltresor"
    semantic_value varchar(80),                  -- optionale Normalform für die Engine
    sort_order     integer NOT NULL DEFAULT 0,
    active         boolean NOT NULL DEFAULT true,
    UNIQUE (question_id, value)
);
CREATE INDEX idx_question_options_q ON question_options(question_id);

-- ----------------------------------------------------------------------------
-- 8. Sichtbarkeitsregeln (dynamische Fragen)
-- ----------------------------------------------------------------------------
-- Trennt UI-Logik strikt von Risikologik. expression = kontrollierte
-- Ausdruckssprache (siehe rule_engine.schema.json).

CREATE TABLE question_visibility_rules (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id uuid NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    priority    integer NOT NULL DEFAULT 100,
    expression  jsonb NOT NULL,
    effect      visibility_effect NOT NULL DEFAULT 'SHOW',
    active      boolean NOT NULL DEFAULT true
);
CREATE INDEX idx_visibility_q ON question_visibility_rules(question_id);

-- ----------------------------------------------------------------------------
-- 9. Antworten
-- ----------------------------------------------------------------------------
-- Typisiert statt „alles Text". Genau ein Wertfeld je Antwort ist befüllt;
-- option_id verweist zusätzlich auf die gewählte Option bei SELECT-Fragen.

CREATE TABLE answers (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id uuid NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    question_id   uuid NOT NULL REFERENCES questions(id) ON DELETE RESTRICT,
    value_boolean boolean,
    value_number  numeric(14,4),
    value_text    text,
    option_id     uuid REFERENCES question_options(id) ON DELETE SET NULL,
    value_date    date,
    answered      boolean NOT NULL DEFAULT false, -- explizit beantwortet? (≠ „leer")
    created_by    uuid REFERENCES users(id),
    created_at    timestamptz NOT NULL DEFAULT now(),
    updated_at    timestamptz NOT NULL DEFAULT now(),
    UNIQUE (assessment_id, question_id)
);
CREATE INDEX idx_answers_assessment ON answers(assessment_id);
CREATE INDEX idx_answers_question   ON answers(question_id);

-- ----------------------------------------------------------------------------
-- 10. Gefährdungen (Hazards)
-- ----------------------------------------------------------------------------
-- GBU: M001..M120 (+ Untereinträge M019a/M019b/M020a/M024a). Cyber: MC1..MC13.

CREATE TABLE hazards (
    id                 uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    code               varchar(20) NOT NULL UNIQUE,   -- „M032", „MC4"
    domain             domain_type NOT NULL,
    title              text NOT NULL,
    description        text,
    category           varchar(80),                   -- fachliche Gruppierung (NOTRUF, …)
    -- Aggregation ist eine EIGENSCHAFT DER GEFÄHRDUNG (Delta 4): z. B. M087
    -- Asbest = ANY über vier Ortsfragen. Eine Regel darf sie überschreiben
    -- (evaluation_rules.aggregation_type), erbt sie aber standardmäßig von hier.
    aggregation_type   aggregation_type NOT NULL DEFAULT 'NONE',
    evaluation_mode    evaluation_mode  NOT NULL DEFAULT 'STANDARD',
    active             boolean NOT NULL DEFAULT true,
    not_implemented    boolean NOT NULL DEFAULT false, -- z. B. MC13 im Original
    default_sort_order integer NOT NULL DEFAULT 0,
    created_at         timestamptz NOT NULL DEFAULT now(),
    updated_at         timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_hazards_domain ON hazards(domain);

-- ----------------------------------------------------------------------------
-- 11. Fragen ↔ Gefährdungen (m:n, mit Rolle) – zentrale Tabelle
-- ----------------------------------------------------------------------------

CREATE TABLE hazard_questions (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    hazard_id           uuid NOT NULL REFERENCES hazards(id) ON DELETE CASCADE,
    question_id         uuid NOT NULL REFERENCES questions(id) ON DELETE RESTRICT,
    role                hazard_question_role NOT NULL,
    -- Pflicht-Sein ist gefährdungsspezifisch (Delta 4): dieselbe Frage kann
    -- hier ALWAYS und in einer anderen Gefährdung NEVER sein. Bei ALWAYS und
    -- fehlender Antwort -> Gefährdung INCOMPLETE (nie NO_RISK).
    required_mode       required_mode NOT NULL DEFAULT 'NEVER',
    required_expression jsonb,        -- nur bei required_mode = CONDITIONAL
    sort_order          integer NOT NULL DEFAULT 0,
    notes               text,
    UNIQUE (hazard_id, question_id, role),
    CHECK (required_mode <> 'CONDITIONAL' OR required_expression IS NOT NULL)
);
CREATE INDEX idx_hq_hazard   ON hazard_questions(hazard_id);
CREATE INDEX idx_hq_question ON hazard_questions(question_id);

-- ----------------------------------------------------------------------------
-- 12. Bewertungsregeln
-- ----------------------------------------------------------------------------
-- Jede Gefährdung besitzt in einer Regelversion mehrere priorisierte Regeln.
-- Die höchste zutreffende priority gewinnt. condition_expression und
-- applicability_expression = kontrollierte Ausdruckssprache (JSONB).

CREATE TABLE evaluation_rules (
    id                       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_version_id          uuid NOT NULL REFERENCES rule_versions(id) ON DELETE CASCADE,
    hazard_id                uuid NOT NULL REFERENCES hazards(id) ON DELETE CASCADE,
    code                     varchar(40) NOT NULL,       -- „M032-R001"
    priority                 integer NOT NULL DEFAULT 100,
    applicability_expression jsonb,                       -- NULL = immer anwendbar
    condition_expression     jsonb NOT NULL,              -- Trigger/Bedingung
    result_status            risk_status NOT NULL,
    aggregation_type         aggregation_type,            -- NULL = von hazards erben
    active                   boolean NOT NULL DEFAULT true,
    evidence_level           evidence_level NOT NULL DEFAULT 'DIRECT',
    origin                   rule_origin NOT NULL DEFAULT 'RECONSTRUCTED_ORIGINAL',
    quality_status           quality_status NOT NULL DEFAULT 'REVIEW_REQUIRED',
    notes                    text,
    created_at               timestamptz NOT NULL DEFAULT now(),
    updated_at               timestamptz NOT NULL DEFAULT now(),
    UNIQUE (rule_version_id, code)
);
CREATE INDEX idx_rules_version ON evaluation_rules(rule_version_id);
CREATE INDEX idx_rules_hazard  ON evaluation_rules(hazard_id);
CREATE INDEX idx_rules_prio    ON evaluation_rules(rule_version_id, hazard_id, priority DESC);

-- Optional normalisierte Einzelbedingungen (Alternative/Ergänzung zum JSONB-
-- Ausdruck; für Admin-Auswertungen „welche Regel nutzt Frage X?"). Der
-- JSONB-Ausdruck in evaluation_rules bleibt die maßgebliche Auswertungsquelle.
CREATE TABLE rule_conditions (
    id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_rule_id uuid NOT NULL REFERENCES evaluation_rules(id) ON DELETE CASCADE,
    question_id      uuid NOT NULL REFERENCES questions(id) ON DELETE RESTRICT,
    operator         varchar(20) NOT NULL,       -- EQ/NEQ/GT/GTE/LT/LTE/IN/ANSWERED/…
    expected_value   varchar(200),
    group_key        varchar(40),                -- optionale Verknüpfung (ALL/ANY-Gruppe)
    sort_order       integer NOT NULL DEFAULT 0
);
CREATE INDEX idx_rule_conditions_rule ON rule_conditions(evaluation_rule_id);
CREATE INDEX idx_rule_conditions_q    ON rule_conditions(question_id);

-- ----------------------------------------------------------------------------
-- 13. Pflichtantworten – Hinweis
-- ----------------------------------------------------------------------------
-- Pflicht-Sein liegt bewusst NICHT auf Regel-Ebene, sondern gefährdungs-
-- spezifisch in hazard_questions.required_mode (Delta 4). Damit ist der
-- PARTIAL_EVALUATION_BUG strukturell ausgeschlossen: eine ALWAYS-Pflichtfrage
-- ohne Antwort führt zu INCOMPLETE, während ein Ortsblock (required_mode =
-- NEVER, evaluation_mode = PARTIAL_ALLOWED) mit einer einzigen Ja-Antwort
-- bewertet wird. Eine eigene rule_required_questions-Tabelle entfällt.

-- ----------------------------------------------------------------------------
-- 14. Maßnahmen
-- ----------------------------------------------------------------------------

CREATE TABLE measures (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    code           varchar(60) NOT NULL UNIQUE,
    title          text NOT NULL,
    description    text,
    type           measure_type NOT NULL,
    priority_class varchar(20),        -- z. B. SOFORT / KURZFRISTIG / MITTELFRISTIG
    active         boolean NOT NULL DEFAULT true,
    created_at     timestamptz NOT NULL DEFAULT now(),
    updated_at     timestamptz NOT NULL DEFAULT now()
);

-- ----------------------------------------------------------------------------
-- 15. Regel ↔ Maßnahme (mit UND/ODER-Gruppen und Bedingung)
-- ----------------------------------------------------------------------------
-- Erlaubt: „Maßnahme A ODER B  UND  organisatorische Übergangsmaßnahme C".

CREATE TABLE rule_measures (
    id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_rule_id   uuid NOT NULL REFERENCES evaluation_rules(id) ON DELETE CASCADE,
    measure_id           uuid NOT NULL REFERENCES measures(id) ON DELETE RESTRICT,
    group_id             varchar(40),           -- Maßnahmengruppe
    relation             measure_relation NOT NULL DEFAULT 'SINGLE',
    sort_order           integer NOT NULL DEFAULT 0,
    condition_expression jsonb,                 -- Maßnahme nur unter Bedingung (Modifier)
    mandatory            boolean NOT NULL DEFAULT true,
    notes                text,
    UNIQUE (evaluation_rule_id, measure_id, group_id)
);
CREATE INDEX idx_rule_measures_rule    ON rule_measures(evaluation_rule_id);
CREATE INDEX idx_rule_measures_measure ON rule_measures(measure_id);

-- ----------------------------------------------------------------------------
-- 16. Bewertungsresultat (revisionssicherer Snapshot je Gefährdung)
-- ----------------------------------------------------------------------------
-- input_snapshot friert die tatsächlich verwendeten Antworten ein, damit ein
-- fertiger Bericht exakt reproduzierbar bleibt.

CREATE TABLE evaluation_results (
    id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id     uuid NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    hazard_id         uuid NOT NULL REFERENCES hazards(id) ON DELETE RESTRICT,
    status            risk_status NOT NULL,            -- effektiv (nach Override)
    automatic_status  risk_status NOT NULL,            -- Engine-Ergebnis
    manual_status     risk_status,                     -- gesetzt bei Override
    is_overridden     boolean NOT NULL DEFAULT false,
    matched_rule_id   uuid REFERENCES evaluation_rules(id) ON DELETE SET NULL,
    rule_version_id   uuid NOT NULL REFERENCES rule_versions(id) ON DELETE RESTRICT,
    input_snapshot    jsonb NOT NULL DEFAULT '{}'::jsonb,
    evaluated_at      timestamptz NOT NULL DEFAULT now(),
    UNIQUE (assessment_id, hazard_id)
);
CREATE INDEX idx_results_assessment ON evaluation_results(assessment_id);
CREATE INDEX idx_results_hazard     ON evaluation_results(hazard_id);
CREATE INDEX idx_results_status     ON evaluation_results(assessment_id, status);

-- ----------------------------------------------------------------------------
-- 17. Manuelle fachliche Übersteuerung (mit Pflichtbegründung)
-- ----------------------------------------------------------------------------

CREATE TABLE manual_overrides (
    id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_result_id uuid NOT NULL REFERENCES evaluation_results(id) ON DELETE CASCADE,
    original_status      risk_status NOT NULL,
    override_status      risk_status NOT NULL,
    reason               text NOT NULL,            -- keine Änderung ohne Begründung
    created_by           uuid REFERENCES users(id),
    created_at           timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_overrides_result ON manual_overrides(evaluation_result_id);

-- ----------------------------------------------------------------------------
-- 18. Fotos & Bemerkungen (an Frage ODER Gefährdung)
-- ----------------------------------------------------------------------------

CREATE TABLE photos (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id uuid NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    question_id   uuid REFERENCES questions(id) ON DELETE SET NULL,
    hazard_id     uuid REFERENCES hazards(id) ON DELETE SET NULL,
    file_key      varchar(400) NOT NULL,      -- Objektspeicher-Schlüssel
    caption       text,
    taken_at      timestamptz,
    created_by    uuid REFERENCES users(id),
    created_at    timestamptz NOT NULL DEFAULT now(),
    CHECK (question_id IS NOT NULL OR hazard_id IS NOT NULL)
);
CREATE INDEX idx_photos_assessment ON photos(assessment_id);

CREATE TABLE remarks (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_id uuid NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    question_id   uuid REFERENCES questions(id) ON DELETE SET NULL,
    hazard_id     uuid REFERENCES hazards(id) ON DELETE SET NULL,
    text          text NOT NULL,
    created_by    uuid REFERENCES users(id),
    created_at    timestamptz NOT NULL DEFAULT now(),
    updated_at    timestamptz NOT NULL DEFAULT now(),
    CHECK (question_id IS NOT NULL OR hazard_id IS NOT NULL)
);
CREATE INDEX idx_remarks_assessment ON remarks(assessment_id);

-- ----------------------------------------------------------------------------
-- 19. Norm-/Quellenbezug
-- ----------------------------------------------------------------------------

CREATE TABLE source_references (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type   source_type NOT NULL,
    document_code varchar(80) NOT NULL,        -- „TRBS 3121", „EN 81-20"
    title         varchar(300),
    edition       varchar(60),
    section       varchar(120),
    description    text,
    UNIQUE (source_type, document_code, section)
);

CREATE TABLE hazard_sources (
    hazard_id           uuid NOT NULL REFERENCES hazards(id) ON DELETE CASCADE,
    source_reference_id uuid NOT NULL REFERENCES source_references(id) ON DELETE CASCADE,
    PRIMARY KEY (hazard_id, source_reference_id)
);

CREATE TABLE rule_sources (
    evaluation_rule_id  uuid NOT NULL REFERENCES evaluation_rules(id) ON DELETE CASCADE,
    source_reference_id uuid NOT NULL REFERENCES source_references(id) ON DELETE CASCADE,
    PRIMARY KEY (evaluation_rule_id, source_reference_id)
);

-- ----------------------------------------------------------------------------
-- 20. Regel-Templates (z. B. MC4–MC9 „DIGITAL_COMPONENT_ACCESS")
-- ----------------------------------------------------------------------------

CREATE TABLE rule_templates (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    code                varchar(80) NOT NULL UNIQUE,   -- DIGITAL_COMPONENT_ACCESS
    domain              domain_type NOT NULL,
    template_definition jsonb NOT NULL,                -- parametrierbarer Regelrumpf
    description         text
);

CREATE TABLE rule_template_instances (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id uuid NOT NULL REFERENCES rule_templates(id) ON DELETE CASCADE,
    hazard_id   uuid NOT NULL REFERENCES hazards(id) ON DELETE CASCADE,
    parameters  jsonb NOT NULL,                        -- konkrete Frage-Codes je Slot
    UNIQUE (template_id, hazard_id)
);

-- ----------------------------------------------------------------------------
-- 21. Ortsmatrix (optional) – Mangelart × Ort
-- ----------------------------------------------------------------------------
-- Erlaubt es, „a-Fragen" (a1xx Zugang, a2xx TWR, a3xx Fahrkorb/Schacht,
-- a4xx Grube) als Kombination defect_type × location zu modellieren, statt
-- hunderte identischer Spezialfälle einzeln zu pflegen.

-- Orte der Ortsmatrix (a1xx Zugang, a2xx TWR, a3xx Fahrkorb/Schacht,
-- a4xx Grube). Delta 4 bestätigt das a-ID-Schema (u. a. a447 = brandfördernd
-- in der Grube); die letzte Ziffer ist eine laufende Nummer je Ort.
CREATE TABLE hazard_locations (
    id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    code  varchar(40) NOT NULL UNIQUE,   -- ACCESS/MACHINE_ROOM/SHAFT_CAR/PIT/OTHER
    title varchar(120) NOT NULL,
    sort_order integer NOT NULL DEFAULT 0
);

CREATE TABLE defect_types (
    id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    code  varchar(60) NOT NULL UNIQUE,   -- ASBESTOS/CONTAMINATION/FLAMMABLE_MATERIAL/…
    title varchar(160) NOT NULL,
    domain domain_type NOT NULL DEFAULT 'GBU'
);

-- Optionale Zuordnung einer Frage zu (Mangelart, Ort), für generierte
-- Matrix-Fragebögen. Nicht zwingend – „normale" Fragen brauchen das nicht.
-- Beispiel M103: FLAMMABLE_MATERIAL × {MACHINE_ROOM,SHAFT_CAR,PIT,OTHER}.
CREATE TABLE question_defect_context (
    question_id    uuid NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    defect_type_id uuid NOT NULL REFERENCES defect_types(id) ON DELETE CASCADE,
    location_id    uuid NOT NULL REFERENCES hazard_locations(id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, defect_type_id, location_id)
);

-- ----------------------------------------------------------------------------
-- 22. Zusammenfassung je Assessment (berechenbar/gecacht)
-- ----------------------------------------------------------------------------

CREATE TABLE assessment_summary (
    assessment_id           uuid PRIMARY KEY REFERENCES assessments(id) ON DELETE CASCADE,
    questions_total         integer NOT NULL DEFAULT 0,
    questions_answered      integer NOT NULL DEFAULT 0,
    hazards_total           integer NOT NULL DEFAULT 0,
    hazards_high            integer NOT NULL DEFAULT 0,
    hazards_medium          integer NOT NULL DEFAULT 0,
    hazards_low             integer NOT NULL DEFAULT 0,
    hazards_no_risk         integer NOT NULL DEFAULT 0,
    hazards_not_applicable  integer NOT NULL DEFAULT 0,
    hazards_incomplete      integer NOT NULL DEFAULT 0,
    gbu_evaluable_pct       numeric(5,2),
    cyber_evaluable_pct     numeric(5,2),
    computed_at             timestamptz NOT NULL DEFAULT now()
);

-- ----------------------------------------------------------------------------
-- 23. Audit-Log (Daten) + Regeländerungs-Log (Regelwerk)
-- ----------------------------------------------------------------------------

CREATE TABLE audit_log (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id     uuid REFERENCES tenants(id) ON DELETE SET NULL,
    assessment_id uuid REFERENCES assessments(id) ON DELETE SET NULL,
    user_id       uuid REFERENCES users(id) ON DELETE SET NULL,
    entity_type   varchar(60) NOT NULL,
    entity_id     uuid,
    action        audit_action NOT NULL,
    old_value     jsonb,
    new_value     jsonb,
    "timestamp"   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_audit_assessment ON audit_log(assessment_id);
CREATE INDEX idx_audit_entity     ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_time       ON audit_log("timestamp");

CREATE TABLE rule_change_log (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id         uuid REFERENCES evaluation_rules(id) ON DELETE SET NULL,
    rule_version_id uuid REFERENCES rule_versions(id) ON DELETE SET NULL,
    change_type     varchar(40) NOT NULL,      -- CREATE/UPDATE/DEACTIVATE/…
    old_rule        jsonb,
    new_rule        jsonb,
    reason          text,
    changed_by      uuid REFERENCES users(id) ON DELETE SET NULL,
    changed_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_rule_change_rule ON rule_change_log(rule_id);

-- ============================================================================
-- Hinweise zur Auswertung (siehe Doku „GBU 4.0 – Datenmodell & Regelengine"):
--   Reihenfolge je Gefährdung:
--     1) Applicability  -> UNKNOWN=INCOMPLETE, FALSE=NOT_APPLICABLE
--     2) Pflichtfragen (hazard_questions.required_mode = ALWAYS, bzw.
--        CONDITIONAL wenn required_expression zutrifft) -> fehlt eine ->
--        INCOMPLETE. Ortsblöcke mit required_mode = NEVER blockieren nicht.
--     3) Trigger/Regeln (ggf. Aggregation aus hazards.aggregation_type, z. B.
--        ANY/MAXIMUM) -> keine passende Regel -> NO_RISK
--     4) Kompensation/Modifier berücksichtigen
--     5) höchste priority der zutreffenden Regeln gewinnt -> result_status
--     6) evaluation_results + input_snapshot schreiben
--   Finalisierung: hazards_incomplete > 0 blockiert FINAL (außer bewusste,
--   begründete Freigabe).
-- ============================================================================

-- DROP-Reihenfolge (umgekehrt), falls das Schema zurückgerollt werden muss:
--   question_defect_context, defect_types, hazard_locations,
--   rule_template_instances, rule_templates,
--   rule_change_log, audit_log, assessment_summary,
--   rule_sources, hazard_sources, source_references,
--   remarks, photos, manual_overrides, evaluation_results,
--   rule_measures, measures, rule_conditions,
--   evaluation_rules, hazard_questions, hazards,
--   answers, question_visibility_rules, question_options, questions,
--   question_categories, assessments, rule_versions, assets, users, tenants
--   und danach die ENUM-Typen (DROP TYPE …).
