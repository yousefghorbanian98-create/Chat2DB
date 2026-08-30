"""Differential self-update for an installed Muscle Paradise prefix.

An install prefix looks like::

    <prefix>/app/backend/...      <- the code
    <prefix>/app/studio/...       <- prebuilt shell
    <prefix>/app/assets|packs/... <- runtime assets
    <prefix>/venv/                <- NOT touched unless requirements changed
    <prefix>/bin/mp               <- NOT touched
    <prefix>/mp.db                <- NEVER touched (the gym's data)

`build_dist.sh` writes a ``MANIFEST.json`` (version + sha256 per file) into the
package. The updater diffs the installed manifest against the new one and
touches only the files that actually differ — everything else, including the
database, is left alone. Apply is transactional: the current tree is archived
first and restored if verification fails.

Usage:
    python -m app.updater --prefix ~/.muscle-paradise --from ./mp-app-0.20.0 --dry-run
    python -m app.updater --prefix ~/.muscle-paradise --from ./mp-app-0.20.0
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
from dataclasses import dataclass, field
from pathlib import Path

MANIFEST_NAME = "MANIFEST.json"
#: Relative to the prefix. The updater never writes inside these.
PROTECTED = ("venv", "bin")
#: Database files are data, not code. Matched by name anywhere under the prefix.
PROTECTED_SUFFIXES = (".db", ".db-wal", ".db-shm")
_SKIP_DIR_NAMES = {"__pycache__", ".pytest_cache"}
_CHUNK = 1 << 20


def file_hash(path: Path) -> str:
    """SHA-256 of a file, streamed so a large bundle never lands in memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path, only: tuple[str, ...] | None = None) -> dict[str, str]:
    """Map every file under ``root`` to its sha256, keyed by POSIX relative path.

    Args:
        root: directory to walk.
        only: when given, only these top-level entries are included — used to
            describe just the part of a package that an install actually copies
            (installer scripts and INSTALL.md stay out of the manifest).

    Caches and the manifest itself are excluded so a rebuilt tree compares clean.
    """
    entries: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if only is not None and (not rel.parts or rel.parts[0] not in only):
            continue
        if any(part in _SKIP_DIR_NAMES for part in rel.parts):
            continue
        if rel.name == MANIFEST_NAME:
            continue
        entries[rel.as_posix()] = file_hash(path)
    return entries


#: The package entries an install copies into <prefix>/app.
INSTALLED_TOP_LEVEL = ("backend", "studio", "assets", "packs")


def write_manifest(root: Path, version: str, only: tuple[str, ...] | None = None) -> Path:
    """Write ``MANIFEST.json`` for ``root`` and return its path."""
    payload = {"version": version, "files": build_manifest(root, only)}
    target = root / MANIFEST_NAME
    target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return target


def load_manifest(path: Path) -> dict[str, str]:
    """Read a manifest's ``files`` map; a missing manifest means "nothing known"."""
    if not path.is_file():
        return {}
    parsed = json.loads(path.read_text(encoding="utf-8"))
    files = parsed.get("files", {})
    if not isinstance(files, dict):
        raise ValueError(f"{path}: manifest has no 'files' map")
    return {str(k): str(v) for k, v in files.items()}


def read_version(path: Path) -> str:
    """Read the version a manifest was built for ('' when unknown)."""
    if not path.is_file():
        return ""
    return str(json.loads(path.read_text(encoding="utf-8")).get("version", ""))


@dataclass(frozen=True)
class UpdatePlan:
    """Which files an update would touch, and which it would leave alone."""

    added: tuple[str, ...] = ()
    changed: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()
    unchanged: int = 0

    @property
    def is_empty(self) -> bool:
        return not (self.added or self.changed or self.removed)

    def describe(self) -> str:
        return (
            f"{len(self.added)} new, {len(self.changed)} changed, "
            f"{len(self.removed)} removed, {self.unchanged} unchanged"
        )


def diff_manifests(old: dict[str, str], new: dict[str, str]) -> UpdatePlan:
    """Compute the minimal file set that separates two manifests."""
    added = tuple(sorted(k for k in new if k not in old))
    removed = tuple(sorted(k for k in old if k not in new))
    changed = tuple(sorted(k for k in new if k in old and new[k] != old[k]))
    unchanged = sum(1 for k in new if k in old and new[k] == old[k])
    return UpdatePlan(added=added, changed=changed, removed=removed, unchanged=unchanged)


def _is_protected(rel: str) -> bool:
    """True for paths the updater must never create, replace or delete."""
    parts = Path(rel).parts
    if parts and parts[0] in PROTECTED:
        return True
    return any(rel.endswith(suffix) for suffix in PROTECTED_SUFFIXES)


@dataclass
class UpdateReport:
    """Outcome of an apply (or of a dry run, where ``applied`` stays False)."""

    plan: UpdatePlan
    applied: bool = False
    from_version: str = ""
    to_version: str = ""
    dependencies_refreshed: bool = False
    notes: list[str] = field(default_factory=list)


def _backup_app(app_dir: Path, prefix: Path) -> Path:
    """Snapshot the current app tree so a failed apply can be undone."""
    archive = prefix / f".app-backup-{read_version(app_dir / MANIFEST_NAME) or 'unknown'}.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(app_dir, arcname="app")
    return archive


def _restore_app(archive: Path, prefix: Path) -> None:
    """Roll the app tree back to a snapshot taken by ``_backup_app``."""
    app_dir = prefix / "app"
    shutil.rmtree(app_dir, ignore_errors=True)
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(prefix)  # noqa: S202 - archive was written by us this run


def _copy_tree(source: Path, app_dir: Path, plan: UpdatePlan) -> None:
    """Materialise the planned additions/changes and drop the planned removals."""
    for rel in (*plan.added, *plan.changed):
        if _is_protected(rel):
            raise ValueError(f"refusing to write protected path: {rel}")
        target = app_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / rel, target)
    for rel in plan.removed:
        if _is_protected(rel):
            raise ValueError(f"refusing to remove protected path: {rel}")
        (app_dir / rel).unlink(missing_ok=True)


def apply_update(prefix: Path, source: Path, *, dry_run: bool = False) -> UpdateReport:
    """Update ``prefix`` from an unpacked package ``source``.

    Only files whose sha256 differs are written. ``mp.db`` and ``venv`` are
    never touched; the venv is only refreshed when a requirements file changed.
    A dry run computes and returns the plan without writing anything.

    Raises:
        ValueError: if the source is not a usable package, or the update would
            write a protected path.
    """
    src_manifest_path = source / MANIFEST_NAME
    if not src_manifest_path.is_file():
        raise ValueError(f"{source} has no {MANIFEST_NAME} — not an MP package")

    app_dir = prefix / "app"
    dst_manifest_path = app_dir / MANIFEST_NAME
    old_files = load_manifest(dst_manifest_path)
    if not old_files and app_dir.is_dir():
        # An install from before manifests existed: take the real tree as the
        # baseline, so removals are computed and verification stays exact.
        old_files = build_manifest(app_dir)
    new_files = load_manifest(src_manifest_path)
    plan = diff_manifests(old_files, new_files)
    report = UpdateReport(
        plan=plan,
        from_version=read_version(dst_manifest_path),
        to_version=read_version(src_manifest_path),
    )
    if dry_run:
        report.notes.append("dry run — nothing was written")
        return report
    if plan.is_empty and report.from_version == report.to_version:
        report.notes.append("already up to date")
        return report

    app_dir.mkdir(parents=True, exist_ok=True)
    archive = _backup_app(app_dir, prefix) if app_dir.exists() else None
    try:
        _copy_tree(source, app_dir, plan)
        actual = build_manifest(app_dir)
        if actual != new_files:
            mismatch = sorted(set(actual) ^ set(new_files))[:5]
            raise ValueError(f"post-update verification failed, e.g. {mismatch}")
        shutil.copy2(src_manifest_path, dst_manifest_path)
    except Exception:
        if archive is not None:
            _restore_app(archive, prefix)
            report.notes.append("failed — previous version restored")
        raise

    report.applied = True
    report.dependencies_refreshed = _refresh_dependencies(prefix, plan)
    if archive is not None:
        archive.unlink(missing_ok=True)
    return report


def _refresh_dependencies(prefix: Path, plan: UpdatePlan) -> bool:
    """Re-run pip only when a requirements file actually changed."""
    touched = {p for p in (*plan.added, *plan.changed) if "requirements" in Path(p).name}
    if not touched:
        return False
    venv_py = prefix / "venv" / "bin" / "python"
    req = prefix / "app" / "backend" / "requirements-runtime.txt"
    if not venv_py.is_file() or not req.is_file():
        return False
    subprocess.run(  # noqa: S603 - fixed argv, no shell
        [str(venv_py), "-m", "pip", "install", "--quiet", "-r", str(req)], check=True
    )
    return True


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns a process exit code."""
    parser = argparse.ArgumentParser(prog="mp update", description=__doc__)
    parser.add_argument("--prefix", required=True, help="install prefix (e.g. ~/.muscle-paradise)")
    parser.add_argument("--from", dest="source", required=True, help="unpacked new package dir")
    parser.add_argument("--dry-run", action="store_true", help="show the plan, write nothing")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    prefix = Path(args.prefix).expanduser().resolve()
    source = Path(args.source).expanduser().resolve()
    try:
        report = apply_update(prefix, source, dry_run=args.dry_run)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    verb = "would update" if args.dry_run else "updated"
    print(f"{verb} {report.from_version or '(none)'} -> {report.to_version}")
    print(f"  files: {report.plan.describe()}")
    for rel in (*report.plan.added, *report.plan.changed, *report.plan.removed)[:20]:
        print(f"    {rel}")
    if report.dependencies_refreshed:
        print("  dependencies: refreshed (requirements changed)")
    for note in report.notes:
        print(f"  {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
