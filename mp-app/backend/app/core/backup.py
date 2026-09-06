"""Password-encrypted backup + verified restore (map §14 Phase 6, security §15).

Success metric: "restore row counts match". A backup is a Fernet-encrypted,
LZMA-compressed JSON dump of every business table; restore rebuilds the schema
and asserts per-table row counts against the source.
"""

from __future__ import annotations

import base64
import json
import lzma
import os
from typing import Any

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

MAGIC = b"MPBK1\x00"          # MuscleParadise BacKup v1
_PBKDF2_ITERATIONS = 200_000
_EXCLUDE = {"alembic_version"}  # migration bookkeeping, not gym data


class BackupError(Exception):
    """Raised when a backup cannot be created or restored."""


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                     iterations=_PBKDF2_ITERATIONS)
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def _business_tables(engine: Engine) -> list[str]:
    names = [t for t in inspect(engine).get_table_names() if t not in _EXCLUDE]
    return sorted(names)


def _dump_rows(engine: Engine) -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[dict[str, Any]]] = {}
    with engine.connect() as conn:
        for table in _business_tables(engine):
            rows = conn.execute(text(f'SELECT * FROM "{table}"')).mappings().all()
            data[table] = [dict(r) for r in rows]
    return data


def create_backup(engine: Engine, password: str) -> bytes:
    """Return an encrypted backup blob for every business table."""
    if not password:
        raise BackupError("password is required")
    payload = json.dumps(_dump_rows(engine), default=str, separators=(",", ":")).encode()
    salt = os.urandom(16)
    fernet = Fernet(_derive_key(password, salt))
    compressed = lzma.compress(payload)
    return MAGIC + salt + fernet.encrypt(compressed)


def restore_backup(engine: Engine, blob: bytes, password: str) -> dict[str, int]:
    """Decrypt + reload a backup into ``engine``; return per-table row counts.

    Raises:
        BackupError: bad magic, wrong password, or corrupt payload.
    """
    if not blob.startswith(MAGIC):
        raise BackupError("not a MuscleParadise backup (bad magic)")
    salt = blob[len(MAGIC):len(MAGIC) + 16]
    body = blob[len(MAGIC) + 16:]
    try:
        compressed = Fernet(_derive_key(password, salt)).decrypt(body)
        data = json.loads(lzma.decompress(compressed))
    except InvalidToken as exc:
        raise BackupError("wrong password or corrupt backup") from exc
    except (lzma.LZMAError, ValueError) as exc:
        raise BackupError(f"corrupt backup payload: {exc}") from exc

    counts: dict[str, int] = {}
    with engine.begin() as conn:
        # Children before parents on delete; parents before children on insert is
        # handled by inserting in sorted-table order with FKs deferred.
        conn.execute(text("PRAGMA foreign_keys = OFF"))
        for table in sorted(data, reverse=True):
            conn.execute(text(f'DELETE FROM "{table}"'))
        for table in sorted(data):
            rows = data[table]
            counts[table] = len(rows)
            if not rows:
                continue
            cols = ", ".join(f'"{c}"' for c in rows[0].keys())
            placeholders = ", ".join(f":{c}" for c in rows[0].keys())
            conn.execute(
                text(f'INSERT INTO "{table}" ({cols}) VALUES ({placeholders})'),
                rows,
            )
        conn.execute(text("PRAGMA foreign_keys = ON"))
    return counts


def verify_row_counts(engine: Engine, expected: dict[str, int]) -> dict[str, int]:
    """Return {table: actual} and raise if any count differs from ``expected``."""
    actual: dict[str, int] = {}
    with engine.connect() as conn:
        for table, want in expected.items():
            got = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar_one()
            actual[table] = int(got)
            if int(got) != want:
                raise BackupError(f"row count mismatch for {table}: {got} != {want}")
    return actual
