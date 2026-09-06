"""Migration primitives, kept separate from the runner to avoid a cycle.

``app/migrations/__init__.py`` imports concrete migration modules; those modules
need ``Migration`` — so the dataclass lives here (leaf module, no imports from
the package).
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass


class MigrationError(RuntimeError):
    """Base class for migration failures."""


class MigrationDriftError(MigrationError):
    """An already-applied migration's SQL no longer matches its checksum."""


@dataclass(frozen=True)
class Migration:
    """One ordered schema change."""

    version: str
    label: str
    statements: Sequence[str]

    @property
    def checksum(self) -> str:
        """SHA-256 over the exact SQL, so drift is detectable."""
        payload = "\n;\n".join(self.statements).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()
