"""Tests of the delivery package only. These never execute MP application code."""
from __future__ import annotations

import csv
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parent
PAYLOAD = BASE / "pwa-arena-v1"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preflight = load_module("handoff_preflight", PAYLOAD / "scripts/preflight.py")
# Historical v1 remains byte-frozen; its tests do not validate v2 source coverage.
builder = load_module("handoff_builder", BASE / "build_pwa_handoff.py").Bundle("1.0.0")


def fixture(root: Path) -> None:
    for name in preflight.REQUIRED_FILES:
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("fixture", encoding="utf-8")
    for name in preflight.REQUIRED_DIRS:
        (root / name).mkdir(parents=True, exist_ok=True)
    for name in preflight.FEATURES:
        (root / "mp-app/client/lib/features" / name).mkdir(parents=True)
    routes = {"paths": ["/fixture"], "operations": [{"method": "GET", "path": "/fixture", "roles": sorted(preflight.KNOWN_ROLES), "always_roles": []}]}
    (root / "mp-app/backend/api/routes.json").write_text(json.dumps(routes))
    (root / "mp-app/studio/package.json").write_text(json.dumps({"name": "fixture-studio", "version": "0.0.0", "scripts": {"test": "DO_NOT_EXECUTE_FIXTURE"}}))


class PreflightTests(unittest.TestCase):
    def test_missing_product_checkout_is_blocked(self):
        result = preflight.inspect_repository(ROOT)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("mp-app" in text for text in result["problems"]))
        self.assertIn("independent_review", result["checks_not_executed"])

    def test_fixture_inventory_does_not_hardcode_historical_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            result = preflight.inspect_layout(root)
            self.assertEqual(result["problems"], [])
            self.assertEqual(result["static_inventory"]["declared_operations"], 1)

    def test_layout_success_still_requires_git_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            result = preflight.inspect_repository(root)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertFalse(result["git"]["verified_checkout"])

    def test_inventory_success_is_not_qa_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            with patch.object(preflight, "git_metadata", return_value={"verified_checkout": True, "head": "0" * 40}):
                result = preflight.inspect_repository(root)
            self.assertEqual(result["status"], "INVENTORY_OK_NOT_QA")
            self.assertIn("human_approval", result["checks_not_executed"])
            self.assertIn("not AGENT-READY", result["warning"])

    def test_malformed_route_fails_without_echoing_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            (root / "mp-app/backend/api/routes.json").write_text("DO_NOT_ECHO_THIS_INVALID_FIXTURE")
            result = preflight.inspect_layout(root)
            self.assertTrue(result["problems"])
            self.assertNotIn("DO_NOT_ECHO", json.dumps(result))

    def test_empty_operation_inventory_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            (root / "mp-app/backend/api/routes.json").write_text('{"paths": [], "operations": []}')
            self.assertTrue(preflight.inspect_layout(root)["problems"])

    def test_role_change_is_reconciliation_not_grant_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            f = root / "mp-app/backend/api/routes.json"
            content = json.loads(f.read_text())
            content["operations"][0]["roles"] = ["member"]
            f.write_text(json.dumps(content))
            before = f.read_bytes()
            result = preflight.inspect_layout(root)
            self.assertTrue(any("never add grants" in v for v in result["problems"]))
            self.assertEqual(before, f.read_bytes())

    def test_only_allowlisted_manifests_are_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            (root / ".env").write_text("DO_NOT_READ_FIXTURE_ENV")
            (root / "mp.db").write_text("DO_NOT_READ_FIXTURE_DB")
            with patch.object(preflight, "_safe_read", wraps=preflight._safe_read) as reader:
                result = preflight.inspect_layout(root)
            self.assertEqual(result["problems"], [])
            self.assertEqual({call.args[1] for call in reader.call_args_list}, {"mp-app/backend/api/routes.json", "mp-app/studio/package.json"})

    def test_symlink_outside_checkout_is_not_read(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
            root = Path(tmp)
            fixture(root)
            destination = Path(outside) / "fixture.txt"
            destination.write_text('{"paths": [], "operations": []}')
            target = root / "mp-app/backend/api/routes.json"
            target.unlink()
            target.symlink_to(destination)
            result = preflight.inspect_layout(root)
            self.assertTrue(any("safely parse" in v for v in result["problems"]))

    def test_cli_wrong_checkout_exits_two(self):
        result = subprocess.run(["python3", str(PAYLOAD / "scripts/preflight.py"), "--repo", str(ROOT)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "BLOCKED")


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads((PAYLOAD / "PWA_PLAN.json").read_text())
        cls.main = (PAYLOAD / "HANDOFF.fa.md").read_text()

    def test_plan_is_complete_proposed_and_acyclic(self):
        phases = self.plan["plan"]
        self.assertEqual([p["id"] for p in phases], [f"PWA-{i:02d}" for i in range(28)])
        earlier = set()
        for phase in phases:
            self.assertEqual(phase["status"], "PROPOSED")
            self.assertFalse(phase["completion_claim"])
            self.assertEqual(phase["evidence_status"], "NOT_RUN")
            self.assertTrue(set(phase["depends_on"]).issubset(earlier))
            self.assertEqual(set(phase["required_domain_gates"]), {"security", "privacy", "finance", "legal", "product"})
            self.assertEqual(len(phase["acceptance_fa"]), 4)
            earlier.add(phase["id"])

    def test_attempt_budget_has_no_off_by_one(self):
        budget = self.plan["default_budget"]
        self.assertEqual(budget["total_attempts"], 3)
        self.assertEqual(budget["retries"], 2)
        self.assertEqual(budget["wall_clock_minutes"], 90)

    def test_all_historical_decision_ids_reserved_not_invented(self):
        register = json.loads((PAYLOAD / "templates/DECISION_REGISTER.json").read_text())
        self.assertEqual([d["id"] for d in register["historical_decisions"]], [f"D-{i:02d}" for i in range(1, 12)])
        for decision in register["historical_decisions"]:
            self.assertIsNone(decision["original_text"])
            self.assertIsNone(decision["owner_decision"])
            self.assertFalse(decision["mapping_verified"])
        questions = {d["id"] for d in register["new_questions"]}
        self.assertEqual(questions, {f"Q-{i:02d}" for i in range(1, 12)})
        for phase in self.plan["plan"]:
            self.assertTrue(set(phase["requires_owner_questions"]).issubset(questions))

    def test_seventeen_domains_covered_once_in_matrix(self):
        with (PAYLOAD / "templates/FEATURE_PARITY.csv").open() as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 17)
        self.assertEqual({r["feature"] for r in rows}, set(preflight.FEATURES))
        for row in rows:
            self.assertEqual(row["status"], "PROPOSED")
            self.assertEqual(row["evidence"], "NOT_RUN")
            self.assertIn(row["pwa_phase"], self.main)

    def test_main_and_machine_plan_agree(self):
        self.assertNotRegex(self.main, r"\{\{[A-Z_]+\}\}")
        for phase in self.plan["plan"]:
            self.assertIn(phase["id"] + " — " + phase["title_fa"], self.main)
            for criterion in phase["acceptance_fa"]:
                self.assertIn(criterion, self.main)

    def test_source_paths_and_snapshots_have_provenance(self):
        inventory = json.loads((PAYLOAD / "references/MP_SOURCE_INVENTORY.json").read_text())
        self.assertEqual(set(inventory["features"]), set(preflight.FEATURES))
        for phase in self.plan["plan"]:
            for path in phase["source_paths"]:
                self.assertTrue(inventory["verified_plan_source_paths"][path], path)
        for source in json.loads((PAYLOAD / "references/SOURCE_MANIFEST.json").read_text()):
            data = (PAYLOAD / source["package_path"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), source["sha256"])
            self.assertIn(source["commit"], source["url"])

    def test_static_api_inventory_is_consistent_not_execution(self):
        api = json.loads((PAYLOAD / "references/mp-api-routes.snapshot.json").read_text())
        self.assertEqual((len(api["paths"]), len(api["operations"])), (141, 163))
        with (PAYLOAD / "references/MP_API_OPERATIONS.csv").open() as file:
            self.assertEqual(len(list(csv.DictReader(file))), 163)

    def test_node_manifests_have_exact_locked_versions_and_no_lifecycle(self):
        for directory in ("node", "diagram"):
            base = PAYLOAD / "tooling" / directory
            manifest = json.loads((base / "package.json").read_text())
            lock = json.loads((base / "package-lock.json").read_text())
            self.assertTrue(manifest["private"])
            self.assertFalse(manifest.get("scripts"))
            self.assertEqual(lock["packages"][""]["devDependencies"], manifest["devDependencies"])
            for name, version in manifest["devDependencies"].items():
                self.assertRegex(version, r"^\d+\.\d+\.\d+$")
                self.assertEqual(lock["packages"]["node_modules/" + name]["version"], version)

    def test_historical_flowchart_matches_frozen_v1_archive(self):
        # docs/ now publishes the revised v2 diagram; v1 is the historical oracle.
        archive = BASE / "releases" / (builder.NAME + ".zip")
        with zipfile.ZipFile(archive) as bundle:
            for extension in ("md", "mmd", "png", "svg"):
                name = "diagrams/PWA_Finn_Loop_Flow.fa." + extension
                self.assertEqual((PAYLOAD / name).read_bytes(), bundle.read(builder.NAME + "/" + name))

    def test_local_markdown_links_resolve(self):
        for file in PAYLOAD.rglob("*.md"):
            if any(part in {"node_modules", ".cache"} for part in file.parts):
                continue
            content = re.sub(r"```.*?```", "", file.read_text(), flags=re.S)
            for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", content):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                target = target.split("#")[0]
                self.assertTrue((file.parent / target).exists(), f"{file.relative_to(PAYLOAD)} -> {target}")

    def test_offline_html_contains_embedded_image_and_no_scripts(self):
        content = (PAYLOAD / "HANDOFF.fa.html").read_text()
        class Parser(HTMLParser):
            images = []
            scripts = []
            def handle_starttag(self, tag, attrs):
                if tag == "img": self.images.append(dict(attrs).get("src", ""))
                if tag == "script": self.scripts.append(attrs)
        parsed = Parser()
        parsed.feed(content)
        self.assertEqual(len(parsed.images), 1)
        self.assertTrue(parsed.images[0].startswith("data:image/png;base64,"))
        self.assertEqual(parsed.scripts, [])
        self.assertIn('lang="fa" dir="rtl"', content)

    def test_payload_contains_no_runtime_or_private_artifacts(self):
        forbidden = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}")
        for file in builder.payload_files():
            self.assertNotIn("node_modules", file.parts)
            self.assertNotIn(file.suffix.lower(), {".db", ".sqlite", ".apk", ".exe", ".key", ".pem"})
            if file.suffix.lower() in {".md", ".txt", ".json", ".py", ".mjs", ".html", ".yml", ".example"}:
                self.assertFalse(forbidden.search(file.read_text()), str(file.relative_to(PAYLOAD)))

    def test_internal_manifests_validate_every_file(self):
        manifest = json.loads((PAYLOAD / "PACKAGE_MANIFEST.json").read_text())
        for record in manifest["files"]:
            data = (PAYLOAD / record["path"]).read_bytes()
            self.assertEqual(len(data), record["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), record["sha256"])
        actual = {f.relative_to(PAYLOAD).as_posix() for f in builder.payload_files(include_manifests=False)}
        self.assertEqual(actual, {r["path"] for r in manifest["files"]})
        checks = (PAYLOAD / "MANIFEST.sha256").read_text().splitlines()
        expected = {f.relative_to(PAYLOAD).as_posix() for f in builder.payload_files() if f.name != "MANIFEST.sha256"}
        found = set()
        for line in checks:
            sha, name = line.split("  ", 1)
            self.assertEqual(hashlib.sha256((PAYLOAD / name).read_bytes()).hexdigest(), sha)
            found.add(name)
        self.assertEqual(found, expected)

    def test_zip_crc_names_manifest_and_contents(self):
        archive = BASE / "releases" / (builder.NAME + ".zip")
        expected = {builder.NAME + "/" + file.relative_to(PAYLOAD).as_posix(): file.read_bytes() for file in builder.payload_files()}
        with zipfile.ZipFile(archive) as bundle:
            self.assertIsNone(bundle.testzip())
            self.assertEqual(set(bundle.namelist()), set(expected))
            for item in bundle.infolist():
                self.assertFalse(item.filename.startswith("/"))
                self.assertNotIn("..", Path(item.filename).parts)
                self.assertEqual(item.date_time, builder.FIXED_ZIP_TIME)
                self.assertEqual(bundle.read(item), expected[item.filename])

    def test_zip_is_byte_reproducible(self):
        archive = BASE / "releases" / (builder.NAME + ".zip")
        before = archive.read_bytes()
        builder.build_zip()
        self.assertEqual(before, archive.read_bytes())


if __name__ == "__main__":
    unittest.main()
