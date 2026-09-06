"""v002: member self-service PIN (client shell, map §5).

Athletes sign in to the client app with their membership code plus a PIN that a
front-desk writer sets for them. Only the PBKDF2 hash is stored (same scheme as
staff PINs in v001) and the column is never included in any read projection, so
the hash can never leak through the masked client API.
"""

from __future__ import annotations

from app.migrations.base import Migration

_STATEMENTS = (
    "ALTER TABLE members ADD COLUMN pin_hash TEXT",
)

MIGRATION = Migration(
    version="0002_member_pin",
    label="member self-service PIN column",
    statements=_STATEMENTS,
)
