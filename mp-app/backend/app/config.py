"""Runtime configuration.

Deliberately dependency-free (no pydantic-settings): MP must boot on a gym PC
with nothing but the pinned requirements installed.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

#: MP owns 8751. Cutting Edge owns 8742 (see ENGINEERING_MAP_FULL_v1.md §4).
DEFAULT_PORT = 8751
DEFAULT_HOST = "127.0.0.1"
API_PREFIX = "/api/v1"
SERVICE_NAME = "muscle-paradise-core"

# Electron renderer in dev serves from Vite; in prod it loads file://.
_DEFAULT_ORIGINS = (
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "app://mp",
)


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings resolved from the environment."""

    db_path: Path
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    cors_origins: tuple[str, ...] = _DEFAULT_ORIGINS
    gym_name: str = "Muscle Paradise"
    #: Machine-local key for tokens + QR signatures. Empty means "load/create
    #: the file next to the database" (map §15: secrets stay on this machine).
    secret_key: str = ""
    #: Optional directory holding a built Studio shell (`vite build` output).
    #: When set, the core serves it at `/` so one process answers on one port —
    #: the packaged installer's single-service mode. Empty = API only.
    static_dir: str = ""
    #: Optional n8n automation bridge (map §12.8). Never required for core ops.
    automation_enabled: bool = False
    automation_url: str = ""
    automation_secret: str = ""

    @property
    def sqlalchemy_url(self) -> str:
        """SQLite URL with a shared cache-safe absolute path."""
        return f"sqlite:///{self.db_path}"

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> "Settings":
        """Build settings from ``env`` (defaults to ``os.environ``).

        Raises:
            ValueError: if ``MP_PORT`` is not a usable TCP port.
        """
        source = os.environ if env is None else env
        raw_port = source.get("MP_PORT", str(DEFAULT_PORT))
        try:
            port = int(raw_port)
        except ValueError as exc:  # never swallow: surface a clear message
            raise ValueError(f"MP_PORT must be an integer, got {raw_port!r}") from exc
        if not 1 <= port <= 65535:
            raise ValueError(f"MP_PORT out of range (1-65535): {port}")

        db_raw = source.get("MP_DB_PATH")
        db_path = (
            Path(db_raw).expanduser().resolve()
            if db_raw
            else Path.home() / ".muscle-paradise" / "mp.db"
        )

        origins = source.get("MP_CORS_ORIGINS")
        cors = (
            tuple(o.strip() for o in origins.split(",") if o.strip())
            if origins
            else _DEFAULT_ORIGINS
        )

        return cls(
            db_path=db_path,
            host=source.get("MP_HOST", DEFAULT_HOST),
            port=port,
            cors_origins=cors,
            gym_name=source.get("MP_GYM_NAME", "Muscle Paradise"),
            static_dir=source.get("MP_STATIC_DIR", ""),
            secret_key=source.get("MP_SECRET", ""),
            automation_enabled=source.get("MP_AUTOMATION_ENABLED", "") == "1",
            automation_url=source.get("MP_AUTOMATION_URL", ""),
            automation_secret=source.get("MP_AUTOMATION_SECRET", ""),
        )
