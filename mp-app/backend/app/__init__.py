"""Muscle Paradise (MP) local-first core package.

Single gym, single machine, offline-first. The HTTP surface is FastAPI on
port **8751** (Cutting Edge uses 8742 — never collide), the store is SQLite.
"""

from __future__ import annotations

__all__ = ["__version__"]

__version__ = "0.19.0"
