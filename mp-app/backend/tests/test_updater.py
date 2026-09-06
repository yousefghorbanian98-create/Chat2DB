"""Differential updater: minimal file set, data untouched, rollback on failure."""

from __future__ import annotations

import json
import tarfile
from pathlib import Path

import pytest

from app import updater
from app.updater import (
    MANIFEST_NAME,
    UpdatePlan,
    apply_update,
    build_manifest,
    diff_manifests,
    file_hash,
    load_manifest,
    write_manifest,
)


def _pkg(root: Path, files: dict[str, str], version: str = "0.20.0") -> Path:
    """Lay out a fake package directory with a manifest."""
    for rel, body in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    write_manifest(root, version)
    return root


def _installed(prefix: Path, files: dict[str, str], version: str = "0.19.0") -> Path:
    """Lay out a fake installed prefix (app tree + a database)."""
    app = prefix / "app"
    _pkg(app, files, version)
    (prefix / "mp.db").write_text("PRECIOUS GYM DATA", encoding="utf-8")
    return app


def test_manifest_roundtrip_and_hash_stability(tmp_path: Path) -> None:
    root = tmp_path / "tree"
    (root / "backend").mkdir(parents=True)
    (root / "backend" / "a.py").write_text("x = 1\n", encoding="utf-8")
    manifest = write_manifest(root, "1.2.3")

    loaded = load_manifest(manifest)
    assert loaded == {"backend/a.py": file_hash(root / "backend" / "a.py")}
    assert json.loads(manifest.read_text(encoding="utf-8"))["version"] == "1.2.3"
    # the manifest never lists itself, so a rebuild compares clean
    assert MANIFEST_NAME not in build_manifest(root)


def test_diff_is_minimal() -> None:
    old = {"same.py": "aaa", "gone.py": "bbb", "edit.py": "ccc"}
    new = {"same.py": "aaa", "edit.py": "ddd", "fresh.py": "eee"}
    plan = diff_manifests(old, new)
    assert plan == UpdatePlan(added=("fresh.py",), changed=("edit.py",),
                              removed=("gone.py",), unchanged=1)
    assert not plan.is_empty
    assert diff_manifests(old, old).is_empty


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    prefix = tmp_path / "p"
    _installed(prefix, {"backend/a.py": "one"})
    source = _pkg(tmp_path / "src", {"backend/a.py": "two", "backend/b.py": "new"}, "0.20.0")

    report = apply_update(prefix, source, dry_run=True)

    assert report.applied is False
    assert report.plan.changed == ("backend/a.py",)
    assert report.plan.added == ("backend/b.py",)
    assert (prefix / "app" / "backend" / "a.py").read_text(encoding="utf-8") == "one"
    assert not (prefix / "app" / "backend" / "b.py").exists()


def test_apply_touches_only_what_changed_and_spares_the_database(tmp_path: Path) -> None:
    prefix = tmp_path / "p"
    _installed(prefix, {"backend/a.py": "one", "backend/keep.py": "KEEP"})
    source = _pkg(tmp_path / "src", {"backend/a.py": "two", "backend/keep.py": "KEEP"})
    keep = prefix / "app" / "backend" / "keep.py"
    before = keep.stat().st_mtime_ns

    report = apply_update(prefix, source)

    assert report.applied is True
    assert report.plan.changed == ("backend/a.py",)
    assert (prefix / "app" / "backend" / "a.py").read_text(encoding="utf-8") == "two"
    assert keep.stat().st_mtime_ns == before  # an unchanged file is not rewritten
    # the whole point: the gym's data survives an update
    assert (prefix / "mp.db").read_text(encoding="utf-8") == "PRECIOUS GYM DATA"
    assert load_manifest(prefix / "app" / MANIFEST_NAME) == build_manifest(source)


def test_removal_is_applied(tmp_path: Path) -> None:
    prefix = tmp_path / "p"
    _installed(prefix, {"backend/a.py": "one", "backend/old.py": "bye"})
    source = _pkg(tmp_path / "src", {"backend/a.py": "one"})

    report = apply_update(prefix, source)

    assert report.plan.removed == ("backend/old.py",)
    assert not (prefix / "app" / "backend" / "old.py").exists()


def test_protected_path_is_refused_and_the_previous_version_is_restored(tmp_path: Path) -> None:
    prefix = tmp_path / "p"
    _installed(prefix, {"backend/a.py": "one"})
    source = _pkg(tmp_path / "src", {"backend/a.py": "two", "venv/evil.py": "nope"})

    with pytest.raises(ValueError, match="protected"):
        apply_update(prefix, source)

    # rollback really happened: the tree is back to the pre-update contents
    assert (prefix / "app" / "backend" / "a.py").read_text(encoding="utf-8") == "one"
    assert not (prefix / "app" / "venv" / "evil.py").exists()
    assert (prefix / "mp.db").read_text(encoding="utf-8") == "PRECIOUS GYM DATA"


def test_source_without_a_manifest_is_rejected(tmp_path: Path) -> None:
    prefix = tmp_path / "p"
    _installed(prefix, {"backend/a.py": "one"})
    bare = tmp_path / "bare"
    bare.mkdir()

    with pytest.raises(ValueError, match="not an MP package"):
        apply_update(prefix, bare)


def test_up_to_date_is_a_noop(tmp_path: Path) -> None:
    prefix = tmp_path / "p"
    _installed(prefix, {"backend/a.py": "one"}, version="0.20.0")
    source = _pkg(tmp_path / "src", {"backend/a.py": "one"}, "0.20.0")

    report = apply_update(prefix, source)

    assert report.applied is False
    assert "already up to date" in report.notes


def test_first_update_over_an_unrecorded_install_still_verifies(tmp_path: Path) -> None:
    """No manifest on the installed side: everything counts as new, and the
    post-update tree must still match the source exactly."""
    prefix = tmp_path / "p"
    (prefix / "app" / "backend").mkdir(parents=True)
    (prefix / "app" / "backend" / "legacy.py").write_text("old", encoding="utf-8")
    source = _pkg(tmp_path / "src", {"backend/a.py": "one"})

    report = apply_update(prefix, source)

    assert report.from_version == ""
    assert report.plan.added == ("backend/a.py",)
    # with no recorded baseline the real tree is the baseline, so a stale file
    # that the new package does not ship is removed rather than left behind
    assert not (prefix / "app" / "backend" / "legacy.py").exists()
    assert report.plan.removed == ("backend/legacy.py",)
    assert load_manifest(prefix / "app" / MANIFEST_NAME) == build_manifest(source)


def test_cli_dry_run_and_error_paths(tmp_path: Path, capsys) -> None:
    """The `mp update` entry point: a plan on stdout, exit 2 on a bad package."""
    from app.updater import main

    prefix = tmp_path / "p"
    _installed(prefix, {"backend/a.py": "one"})
    source = _pkg(tmp_path / "src", {"backend/a.py": "two"}, "0.20.0")

    assert main(["--prefix", str(prefix), "--from", str(source), "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "would update 0.19.0 -> 0.20.0" in out
    assert "1 new, 1 changed" in out or "0 new, 1 changed" in out
    assert (prefix / "app" / "backend" / "a.py").read_text(encoding="utf-8") == "one"

    assert main(["--prefix", str(prefix), "--from", str(source)]) == 0
    assert "updated 0.19.0 -> 0.20.0" in capsys.readouterr().out
    assert (prefix / "app" / "backend" / "a.py").read_text(encoding="utf-8") == "two"

    empty = tmp_path / "empty"
    empty.mkdir()
    assert main(["--prefix", str(prefix), "--from", str(empty)]) == 2
    assert "not an MP package" in capsys.readouterr().err


@pytest.mark.security
class TestRestoreRejectsUnsafeArchives:
    """A tampered rollback snapshot must not be able to write outside the prefix."""

    def _archive(self, tmp_path: Path, build) -> Path:
        archive = tmp_path / "evil.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            build(tar, tmp_path)
        return archive

    def test_rejects_path_traversal_member(self, tmp_path: Path) -> None:
        payload = tmp_path / "payload"
        payload.write_text("pwned", encoding="utf-8")

        def build(tar, _):
            tar.add(payload, arcname="../../escaped.txt")

        archive = self._archive(tmp_path, build)
        prefix = tmp_path / "prefix"
        prefix.mkdir()
        with pytest.raises(ValueError, match="outside prefix"):
            updater._restore_app(archive, prefix)
        assert not (tmp_path.parent / "escaped.txt").exists()

    def test_rejects_symlink_member(self, tmp_path: Path) -> None:
        link = tmp_path / "link"
        link.symlink_to("/etc/passwd")

        def build(tar, _):
            tar.add(link, arcname="app/link")

        archive = self._archive(tmp_path, build)
        prefix = tmp_path / "prefix2"
        prefix.mkdir()
        with pytest.raises(ValueError, match="link member"):
            updater._restore_app(archive, prefix)

    def test_still_restores_a_legitimate_snapshot(self, tmp_path: Path) -> None:
        prefix = tmp_path / "prefix3"
        app_dir = prefix / "app"
        app_dir.mkdir(parents=True)
        (app_dir / "main.py").write_text("v1", encoding="utf-8")

        archive = prefix / "snap.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(app_dir, arcname="app")

        (app_dir / "main.py").write_text("v2-broken", encoding="utf-8")
        updater._restore_app(archive, prefix)
        assert (app_dir / "main.py").read_text(encoding="utf-8") == "v1"
