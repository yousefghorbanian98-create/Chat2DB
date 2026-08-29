"""Dump the OpenAPI document to stdout (keeps mp-app/openapi.yaml honest).

Usage:
    python -m app.export_openapi > ../openapi.yaml
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from app.config import Settings
from app.main import create_app


def main(argv: list[str] | None = None) -> int:
    """Write the OpenAPI JSON to stdout. Returns a process exit code."""
    argv = sys.argv[1:] if argv is None else argv
    indent = 2 if "--compact" not in argv else 0

    with TemporaryDirectory() as tmp:
        settings = Settings(db_path=Path(tmp) / "export.db")
        app = create_app(settings)
        document = app.openapi()
        app.state  # keep reference for linters; app owns the engine
        document["info"]["x-generated-by"] = "app.export_openapi"

    json.dump(document, sys.stdout, indent=indent, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
