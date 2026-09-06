"""0001_core — every table from ENGINEERING_MAP_FULL_v1.md §8.

Rule from the map: **every** table carries
``id, gym_id, created_at, updated_at, deleted_at, rev``. Soft-delete +
tombstones are mandatory because the sync fabric merges multiple devices.
"""

from __future__ import annotations

from app.migrations.base import Migration

# Shared audit columns, appended to every business table.
_AUDIT = """
    id          INTEGER PRIMARY KEY,
    gym_id      INTEGER NOT NULL REFERENCES gyms(id),
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    deleted_at  TEXT,
    rev         INTEGER NOT NULL DEFAULT 1
"""

# gyms has no parent gym: its own row IS the tenant, so gym_id mirrors id.
# It stays nullable at insert time and an AFTER INSERT trigger self-assigns it
# (see trg_gyms_self_tenant) — NOT NULL here would make seeding impossible.
_GYM_AUDIT = _AUDIT.replace(
    "gym_id      INTEGER NOT NULL REFERENCES gyms(id)", "gym_id      INTEGER"
)


def _table(name: str, columns: str = "", *, audit: str = _AUDIT) -> str:
    """Build a CREATE TABLE statement with the audit columns first."""
    body = audit if not columns else f"{audit},{columns}"
    return f"CREATE TABLE IF NOT EXISTS {name} ({body}\n)"


def _index(name: str, table: str, cols: str) -> str:
    return f"CREATE INDEX IF NOT EXISTS {name} ON {table} ({cols})"


_STATEMENTS: tuple[str, ...] = (
    _table("gyms", "\n    name        TEXT NOT NULL,\n    secret_key  TEXT", audit=_GYM_AUDIT),
    _table("staff", """
    username     TEXT NOT NULL,
    pin_hash     TEXT,
    password_hash TEXT,
    role         TEXT NOT NULL
        CHECK (role IN ('OWNER','ADMIN','TRAINER','RECEPTION','KIOSK')),
    full_name    TEXT,
    active       INTEGER NOT NULL DEFAULT 1"""),
    _table("members", """
    membership_code TEXT NOT NULL,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    sex             TEXT NOT NULL CHECK (sex IN ('male','female')),
    birth_date      TEXT,
    phone           TEXT,
    photo_path      TEXT,
    membership_exp  TEXT,
    guardian_consent INTEGER NOT NULL DEFAULT 0"""),
    _table("member_trainer", """
    member_id  INTEGER NOT NULL REFERENCES members(id),
    trainer_id INTEGER NOT NULL REFERENCES staff(id),
    primary_flag INTEGER NOT NULL DEFAULT 0"""),
    _table("member_injuries", """
    member_id    INTEGER NOT NULL REFERENCES members(id),
    body_region  TEXT NOT NULL,
    side         TEXT CHECK (side IN ('left','right','bilateral',NULL)),
    label        TEXT NOT NULL,
    status       TEXT NOT NULL
        CHECK (status IN ('active','recovering','cleared','chronic')),
    pain_0_10    INTEGER CHECK (pain_0_10 BETWEEN 0 AND 10),
    onset        TEXT,
    cleared      TEXT,
    clinician_note     TEXT,
    member_visible_note TEXT,
    requires_clearance INTEGER NOT NULL DEFAULT 0,
    created_by   INTEGER REFERENCES staff(id)"""),
    _table("member_limitations", """
    member_id              INTEGER NOT NULL REFERENCES members(id),
    contraindicated_pattern TEXT NOT NULL,
    allowed_modification    TEXT,
    note                    TEXT"""),
    _table("body_assessments", """
    member_id   INTEGER NOT NULL REFERENCES members(id),
    protocol    TEXT NOT NULL DEFAULT 'jackson_pollock_7',
    equation    TEXT NOT NULL DEFAULT 'siri',
    weight_kg   REAL NOT NULL,
    height_cm   REAL,
    age_years   INTEGER NOT NULL,
    sites_mm    TEXT NOT NULL,
    sum_mm      REAL NOT NULL,
    body_density REAL NOT NULL,
    body_fat_pct REAL NOT NULL,
    fat_mass_kg REAL NOT NULL,
    lean_mass_kg REAL NOT NULL,
    classification TEXT,
    measured_by INTEGER REFERENCES staff(id),
    payload     TEXT"""),
    _table("exercises", """
    key          TEXT NOT NULL,
    name_en      TEXT NOT NULL,
    name_fa      TEXT,
    category     TEXT,
    equipment    TEXT,
    pattern      TEXT,
    primary_muscles TEXT,
    source       TEXT,
    source_license TEXT"""),
    _table("exercise_contraindications", """
    exercise_id INTEGER NOT NULL REFERENCES exercises(id),
    body_region TEXT NOT NULL,
    pattern     TEXT,
    severity    TEXT NOT NULL DEFAULT 'hard_block'
        CHECK (severity IN ('hard_block','swap','caution'))"""),
    _table("gym_equipment", """
    name     TEXT NOT NULL,
    category TEXT,
    count    INTEGER NOT NULL DEFAULT 1,
    available INTEGER NOT NULL DEFAULT 1"""),
    _table("training_programs", """
    member_id INTEGER NOT NULL REFERENCES members(id),
    title     TEXT NOT NULL,
    status    TEXT NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft','trainer_approved','client_ack','needs_review','archived')),
    source    TEXT NOT NULL DEFAULT 'rules' CHECK (source IN ('rules','ollama','gateway')),
    payload   TEXT NOT NULL,
    judge_score REAL,
    generated_by INTEGER REFERENCES staff(id),
    approved_by  INTEGER REFERENCES staff(id),
    applied_at   TEXT"""),
    _table("nutrition_plans", """
    member_id INTEGER NOT NULL REFERENCES members(id),
    bmr_kcal  REAL,
    tdee_kcal REAL,
    protein_g REAL,
    carbs_g   REAL,
    fat_g     REAL,
    payload   TEXT"""),
    _table("attendance", """
    member_id  INTEGER NOT NULL REFERENCES members(id),
    checked_in TEXT NOT NULL,
    checked_out TEXT,
    method     TEXT NOT NULL DEFAULT 'qr'
        CHECK (method IN ('qr','fingerprint','manual','kiosk')),
    qr_sig     TEXT,
    staff_id   INTEGER REFERENCES staff(id)"""),
    _table("packages", """
    name        TEXT NOT NULL,
    duration_days INTEGER NOT NULL,
    price_rial  INTEGER NOT NULL,
    active      INTEGER NOT NULL DEFAULT 1"""),
    _table("payments", """
    member_id  INTEGER NOT NULL REFERENCES members(id),
    package_id INTEGER REFERENCES packages(id),
    amount_rial INTEGER NOT NULL,
    method     TEXT NOT NULL DEFAULT 'cash'
        CHECK (method IN ('cash','card','transfer','pos')),
    receipt_no TEXT,
    voided     INTEGER NOT NULL DEFAULT 0,
    staff_id   INTEGER REFERENCES staff(id)"""),
    _table("consents", """
    member_id  INTEGER NOT NULL REFERENCES members(id),
    kind       TEXT NOT NULL,
    version    TEXT NOT NULL,
    signed_at  TEXT NOT NULL,
    signature  TEXT"""),
    _table("messages", """
    from_staff_id INTEGER REFERENCES staff(id),
    to_member_id  INTEGER REFERENCES members(id),
    body          TEXT NOT NULL,
    read_at       TEXT"""),
    _table("session_feedback", """
    member_id  INTEGER NOT NULL REFERENCES members(id),
    program_id INTEGER REFERENCES training_programs(id),
    exercise_key TEXT,
    pain_flag  INTEGER NOT NULL DEFAULT 0,
    pain_0_10  INTEGER CHECK (pain_0_10 BETWEEN 0 AND 10),
    note       TEXT"""),
    _table("session_sets", """
    member_id   INTEGER NOT NULL REFERENCES members(id),
    program_id  INTEGER REFERENCES training_programs(id),
    exercise_key TEXT NOT NULL,
    set_index   INTEGER NOT NULL,
    weight_kg   REAL,
    reps        INTEGER,
    rir         INTEGER,
    logged_at   TEXT NOT NULL"""),
    _table("progress_photos", """
    member_id INTEGER NOT NULL REFERENCES members(id),
    path      TEXT NOT NULL,
    shot_kind TEXT,
    taken_at  TEXT"""),
    _table("sync_log", """
    device_id  TEXT,
    direction  TEXT CHECK (direction IN ('push','pull')),
    rev_from   INTEGER,
    rev_to     INTEGER,
    row_count  INTEGER,
    ok         INTEGER NOT NULL DEFAULT 1,
    detail     TEXT"""),
    _table("devices", """
    device_id   TEXT NOT NULL,
    kind        TEXT CHECK (kind IN ('studio','client','kiosk')),
    label       TEXT,
    last_seen   TEXT,
    public_key  TEXT"""),
    _table("knowledge_packs_meta", """
    pack_id     TEXT NOT NULL,
    version     TEXT NOT NULL,
    installed_at TEXT,
    checksum    TEXT"""),
    _table("audit_log", """
    actor_staff_id INTEGER REFERENCES staff(id),
    action         TEXT NOT NULL,
    entity         TEXT,
    entity_id      INTEGER,
    detail         TEXT"""),
    # Hot paths: every list query filters by gym + soft-delete.
    _index("ix_members_gym_live", "members", "gym_id, deleted_at"),
    _index("ix_assessments_member", "body_assessments", "member_id, created_at"),
    _index("ix_attendance_member", "attendance", "member_id, checked_in"),
    _index("ix_programs_member_status", "training_programs", "member_id, status"),
    # A gym row is its own tenant: fill gym_id from id immediately after insert.
    """
    CREATE TRIGGER IF NOT EXISTS trg_gyms_self_tenant
    AFTER INSERT ON gyms
    BEGIN
        UPDATE gyms SET gym_id = id WHERE id = NEW.id AND gym_id IS NULL;
    END
    """,
)

MIGRATION = Migration(
    version="0001_core",
    label="core schema (map §8)",
    statements=_STATEMENTS,
)

#: Table names this migration is responsible for — asserted by tests.
EXPECTED_TABLES: frozenset[str] = frozenset(
    {
        "gyms", "staff", "members", "member_trainer", "member_injuries",
        "member_limitations", "body_assessments", "exercises",
        "exercise_contraindications", "gym_equipment", "training_programs",
        "nutrition_plans", "attendance", "payments", "packages", "consents",
        "messages", "session_feedback", "session_sets", "progress_photos",
        "sync_log", "devices", "knowledge_packs_meta", "audit_log",
    }
)
