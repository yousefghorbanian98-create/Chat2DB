#!/usr/bin/env python3
"""Read-only MP input inventory. A successful inventory is NOT a QA/release gate.

Only allowlisted manifests and paths are read. No source, install, network, DB,
API, test, Git hook or application code is executed. Git metadata commands are
local and fsmonitor is disabled. Never reads .env, credentials or member data.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

FEATURES = (
    "assessment14", "auth", "bodycomp", "chat", "checkin", "classes", "feedback",
    "home", "intake", "notifications", "nutrition", "profile", "progress",
    "shell", "shop", "today", "wallet",
)
REFERENCE_SHA = "c46e792657e361cd09799c896c47149b4a5c4d86"
REQUIRED_FILES = (
    "AGENTS.md", "mp-app/backend/pyproject.toml", "mp-app/backend/requirements.txt",
    "mp-app/backend/api/routes.json", "mp-app/backend/security/rbac.py",
    "mp-app/backend/app/security/route_policy.py", "mp-app/studio/package.json",
    "mp-app/studio/package-lock.json", "mp-app/client/pubspec.yaml",
    "mp-app/studio/src/App.tsx", "mp-app/studio/src/auth/AuthContext.tsx",
    "mp-app/studio/public/manifest.webmanifest", "mp-app/studio/public/sw.js",
    "mp-app/studio/tests/pwa.test.ts", "mp-app/studio/nginx.conf",
    "mp-app/studio/Dockerfile", ".github/workflows/ci.yml", ".github/workflows/web.yml",
)
REQUIRED_DIRS = ("mp-app/backend/modules", "mp-app/client/test", "mp-app/studio/src", "mp-app/studio/electron")
KNOWN_ROLES = {"member", "coach", "reception", "manager", "admin", "super_admin"}
NOT_EXECUTED = [
    "lint", "typecheck", "unit_tests", "live_contract", "authorization",
    "e2e", "sast", "supply_chain", "load", "device", "independent_review",
    "security", "privacy", "finance", "legal", "product", "human_approval",
]


def _safe_read(root: Path, relative: str) -> str:
    target = root / relative
    # Do not follow references outside the selected checkout.
    resolved = target.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("Allowlisted file resolves outside selected checkout")
    if target.stat().st_size > 2_000_000:
        raise ValueError("Allowlisted manifest is unexpectedly large")
    return target.read_text(encoding="utf-8")


def inspect_layout(root: Path) -> dict:
    """Inspect only the expected source layout; does not determine Git authority."""
    problems: list[str] = []
    paths = {name: (root / name).is_file() for name in REQUIRED_FILES}
    for name in REQUIRED_DIRS:
        paths[name + "/"] = (root / name).is_dir()
    for feature in FEATURES:
        name = "mp-app/client/lib/features/" + feature
        paths[name + "/"] = (root / name).is_dir()
    problems.extend("Missing required source: " + name for name, exists in paths.items() if not exists)
    for name, exists in paths.items():
        if exists and not (root / name).resolve().is_relative_to(root.resolve()):
            problems.append("Required path resolves outside selected checkout: " + name)
    counts = {"declared_paths": None, "declared_operations": None}
    roles: list[str] = []
    if paths["mp-app/backend/api/routes.json"]:
        try:
            routes = json.loads(_safe_read(root, "mp-app/backend/api/routes.json"))
            if not isinstance(routes, dict) or not isinstance(routes.get("operations"), list) or not isinstance(routes.get("paths"), list):
                raise ValueError("Unexpected route manifest shape")
            if not routes["operations"]:
                raise ValueError("Empty route operation inventory")
            found_roles: set[str] = set()
            for operation in routes["operations"]:
                if not isinstance(operation, dict):
                    raise ValueError("Unexpected operation shape")
                for key in ("roles", "always_roles"):
                    values = operation.get(key, [])
                    if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                        raise ValueError("Unexpected role declaration shape")
                    found_roles.update(values)
            roles = sorted(found_roles)
            counts = {"declared_paths": len(routes["paths"]), "declared_operations": len(routes["operations"])}
            if not KNOWN_ROLES.issubset(found_roles):
                problems.append("Six known roles were not all observed in this static manifest; reconcile source, never add grants to satisfy this check")
            if found_roles - KNOWN_ROLES:
                problems.append("Additional declared roles require reconciliation; this tool does not authorize role changes")
        except (OSError, ValueError, TypeError):
            problems.append("Cannot safely parse the allowlisted route manifest; no source contents printed")
    studio: dict = {}
    if paths["mp-app/studio/package.json"]:
        try:
            doc = json.loads(_safe_read(root, "mp-app/studio/package.json"))
            studio = {"name": doc.get("name"), "version": doc.get("version"), "script_names": sorted(doc.get("scripts", {}))}
        except (OSError, ValueError, TypeError, AttributeError):
            problems.append("Cannot safely parse the Studio manifest; no source contents printed")
    return {"paths": paths, "static_inventory": counts, "static_roles_not_runtime_proof": roles, "studio_manifest": studio, "problems": problems}


def git_metadata(root: Path) -> dict:
    def command(*args: str) -> str:
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(root), *args],
            check=True, capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip()
    try:
        top = Path(command("rev-parse", "--show-toplevel")).resolve()
        if top != root.resolve():
            return {"verified_checkout": False, "reason": "Selected directory is not the Git checkout root"}
        head = command("rev-parse", "HEAD")
        if not re.fullmatch(r"[0-9a-f]{40,64}", head):
            return {"verified_checkout": False, "reason": "Cannot validate local HEAD"}
        return {
            "verified_checkout": True,
            "head": head,
            "branch": command("branch", "--show-current") or "DETACHED_REQUIRES_SESSION_AUTHORITY",
            "dirty": bool(command("status", "--porcelain", "--ignore-submodules=all")),
            "remote_identity": "NOT_READ_VERIFY_REPOSITORY_AND_AUTHORIZED_BRANCH_IN_HOST",
        }
    except (OSError, subprocess.SubprocessError):
        return {"verified_checkout": False, "reason": "Local Git metadata unavailable; no command output printed"}


def inspect_repository(root: Path) -> dict:
    result = inspect_layout(root)
    git = git_metadata(root)
    if not git["verified_checkout"]:
        result["problems"].append(git["reason"])
    result.update({
        "status": "BLOCKED" if result["problems"] else "INVENTORY_OK_NOT_QA",
        "repo_path": str(root.resolve()),
        "git": git,
        "reference_snapshot": REFERENCE_SHA,
        "reference_relation": "MATCHES_PIN_NOT_QA" if git.get("head") == REFERENCE_SHA else "RECONCILE_CURRENT_SOURCE_DO_NOT_RESET_OR_SWITCH",
        "pwa_product_root": "mp-app/studio/",
        "preservation": "Flutter/Android, their docs/tests/CI/Flutter Web and Electron must remain intact",
        "tool_paths_only_not_executions": {name: shutil.which(name) for name in ("python3", "node", "npm", "git", "chromium", "semgrep", "k6")},
        "checks_not_executed": NOT_EXECUTED,
        "warning": "Source-layout inventory only. This is not AGENT-READY, a runtime test, authorization proof, independent review, or release approval.",
    })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="Authorized MP checkout root; never infer it from this delivery repository")
    args = parser.parse_args()
    result = inspect_repository(args.repo.expanduser().resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
