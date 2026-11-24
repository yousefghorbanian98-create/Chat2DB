"""Exact user-plan coverage and delivery checks. Never runs MP application code.

The literal IDs/titles and source digest below are independent of generated
PWA_PLAN.json. v1's 28-item structural tests cannot satisfy these assertions.
"""
from __future__ import annotations

import copy
import csv
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parent
PAYLOAD = BASE / "pwa-arena-v2"
sys.path.insert(0, str(PAYLOAD / "scripts"))
import sync_plan
import make_roadmap
import validate_package


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preflight = load("v2_preflight", PAYLOAD / "scripts/preflight.py")
builder_module = load("v2_builder", BASE / "build_pwa_handoff.py")
builder = builder_module.Bundle("2.0.0")
PIN = "c46e792657e361cd09799c896c47149b4a5c4d86"
SOURCE_DIGEST = "f05412e24d5faea5df8af73f324ec22958990688fdd3ae0917d001b09dbf9583"
EXPECTED = [
    ("PWA-00", "ثبت تصمیم پلتفرم"),
    ("PWA-01", "ممیزی و crosswalk قابلیت‌ها"),
    ("PWA-02", "تصویب ماتریس نقش و مجوز"),
    ("PWA-03", "سیاست نشست و آفلاین"),
    ("PWA-04", "baseline CI و شواهد"),
    ("PWA-05", "نقشهٔ محافظت از آثار Flutter/Android"),
    ("PWA-10", "تعیین مرز اپ React"),
    ("PWA-11", "مسیرهای URL و deep link"),
    ("PWA-12", "shell نقش‌محور و responsive"),
    ("PWA-13", "RTL، فارسی و دسترس‌پذیری پایه"),
    ("PWA-14", "بازبینی manifest و نصب‌پذیری"),
    ("PWA-15", "سیاست ایمن Service Worker"),
    ("PWA-16", "به‌روزرسانی PWA"),
    ("PWA-17", "fallback مسیرهای SPA در وب‌سرور"),
    ("PWA-20", "ورود OTP مشترک"),
    ("PWA-21", "بازیابی و پایان نشست"),
    ("PWA-22", "هویت کاربر از سرور"),
    ("PWA-23", "route guard و منوی fail-closed"),
    ("PWA-24", "ماتریس آزمون منفی API"),
    ("PWA-30", "shell عضو"),
    ("PWA-31", "حساب و عضویت"),
    ("PWA-32", "تغییر شماره و نشست‌های دستگاه"),
    ("PWA-33", "خانه و برنامهٔ امروز"),
    ("PWA-34", "ثبت اجرای تمرین و feedback"),
    ("PWA-35", "intake و gate برنامه"),
    ("PWA-36", "ارزیابی و روندها"),
    ("PWA-37", "تغذیه و ثبت غذا"),
    ("PWA-38", "کلاس و رزرو"),
    ("PWA-39", "QR حضور"),
    ("PWA-3A", "کیف پول و تاریخچه"),
    ("PWA-3B", "پرداخت دستی/فیش"),
    ("PWA-3C", "فروشگاه عضو"),
    ("PWA-3D", "چت"),
    ("PWA-3E", "صندوق اعلان"),
    ("PWA-3F", "feedback آفلاین، فقط در صورت تصویب"),
    ("PWA-40", "نگاشت صفحه‌های فعلی Studio به مسیرهای جدید"),
    ("PWA-41", "اعضا و پروفایل کارکنان"),
    ("PWA-42", "بازبینی برنامه توسط مربی"),
    ("PWA-43", "کلاس و check-in کارکنان"),
    ("PWA-44", "پرداخت و رسید کارکنان"),
    ("PWA-45", "گزارش مالی و هزینه"),
    ("PWA-46", "تنظیمات، grants و audit"),
    ("PWA-47", "responsive و تعامل‌های کارکنان"),
    ("PWA-50", "browser E2E با دادهٔ مصنوعی"),
    ("PWA-51", "نصب و Service Worker واقعی"),
    ("PWA-52", "سازگاری و دسترس‌پذیری"),
    ("PWA-53", "حملات نقش/مالکیت و persistence"),
    ("PWA-54", "build و انتشار staging"),
    ("PWA-55", "آزمون رگرسیون حفظ Flutter/Android"),
    ("PWA-56", "Go/No-Go"),
]
IDS = [row[0] for row in EXPECTED]


def read_json(name):
    return json.loads((PAYLOAD / name).read_text(encoding="utf-8"))


def fixture(root):
    for name in preflight.REQUIRED_FILES:
        file = root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("READ_ONLY_FIXTURE", encoding="utf-8")
    for name in preflight.REQUIRED_DIRS:
        (root / name).mkdir(parents=True, exist_ok=True)
    for feature in preflight.FEATURES:
        (root / "mp-app/client/lib/features" / feature).mkdir(parents=True)
    (root / "mp-app/backend/api/routes.json").write_text(json.dumps({
        "paths": ["/fixture"],
        "operations": [{"method": "GET", "path": "/fixture", "roles": sorted(preflight.KNOWN_ROLES), "always_roles": []}],
    }))
    (root / "mp-app/studio/package.json").write_text(json.dumps({"name": "fixture", "scripts": {"test": "NEVER_EXECUTE_ME"}}))


def temporary_payload(path):
    shutil.copytree(PAYLOAD, path, dirs_exist_ok=True, ignore=shutil.ignore_patterns("node_modules", "__pycache__", ".cache", ".venv*"))


class ExactSourcePlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = sync_plan.read_source()
        cls.plan = read_json("PWA_PLAN.json")
        cls.tasks = cls.plan["plan"]
        cls.by_id = {r["id"]: r for r in cls.tasks}

    def test_source_transcription_is_frozen_and_has_literal_50_titles(self):
        self.assertEqual(hashlib.sha256((PAYLOAD / "SOURCE_PLAN.fa.md").read_bytes()).hexdigest(), SOURCE_DIGEST)
        self.assertEqual([(r["id"], r["title_fa"]) for r in self.source], EXPECTED)
        self.assertEqual(tuple(IDS), sync_plan.EXPECTED_IDS)

    def test_noncontiguous_inventory_is_not_28_or_56_or_last_id_as_count(self):
        self.assertEqual([r["id"] for r in self.tasks], IDS)
        self.assertEqual(len(set(IDS)), 50)
        self.assertEqual(self.plan["task_count"], 50)
        self.assertEqual(self.plan["phase_counts"], [6, 8, 5, 16, 8, 7])
        self.assertEqual([sum(t["phase"] == n for t in self.tasks) for n in range(6)], [6, 8, 5, 16, 8, 7])
        self.assertNotIn("PWA-06", IDS)
        self.assertTrue(set("PWA-3" + c for c in "ABCDEF").issubset(IDS))
        identity = read_json("PLAN_IDENTITY.json")
        self.assertEqual(identity["expected_task_ids"], IDS)
        self.assertFalse(identity["renumbering_permitted"])
        self.assertEqual(identity["merged_or_dropped_source_tasks"], [])

    def test_exact_title_and_full_acceptance_in_each_plan_record(self):
        for source, task in zip(self.source, self.tasks):
            for field in ("id", "phase", "title_fa", "source_acceptance_fa"):
                self.assertEqual(task[field], source[field], task["id"])
            self.assertEqual(task["acceptance_fa"], [source["source_acceptance_fa"]])

    def test_catalog_preserves_all_headings_and_full_original_boundaries(self):
        catalog = (PAYLOAD / "MICROLOOPS.fa.md").read_text()
        headings = re.findall(r"^### (PWA-[0-9A-F]{2}) — (.+)$", catalog, re.M)
        self.assertEqual(headings, EXPECTED)
        for source in self.source:
            self.assertIn(source["source_acceptance_fa"], catalog)

    def test_sync_output_is_current_and_deterministic(self):
        for name, expected in sync_plan.generated().items():
            self.assertEqual((PAYLOAD / name).read_text(), expected)
        self.assertEqual(sync_plan.generated(), sync_plan.generated())

    def test_dependencies_form_a_dag_with_no_orphans(self):
        visiting, visited = set(), set()
        def visit(task_id):
            self.assertNotIn(task_id, visiting)
            if task_id in visited:
                return
            visiting.add(task_id)
            for dependency in self.by_id[task_id]["depends_on"]:
                self.assertIn(dependency, self.by_id)
                visit(dependency)
            visiting.remove(task_id)
            visited.add(task_id)
        for task_id in IDS:
            visit(task_id)
        self.assertEqual(visited, set(IDS))
        for task_id in ("PWA-01", "PWA-04", "PWA-05"):
            self.assertEqual(self.by_id[task_id]["depends_on"], [])
            self.assertEqual(self.by_id[task_id]["owner_decisions"], [])

    def test_cycle_is_rejected_instead_of_silently_serializing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copy2(PAYLOAD / "SOURCE_PLAN.fa.md", root)
            details = read_json("PLAN_DETAILS.json")
            details["tasks"]["PWA-00"]["depends_on"] = ["PWA-10"]
            (root / "PLAN_DETAILS.json").write_text(json.dumps(details))
            with self.assertRaisesRegex(ValueError, "cycle"):
                sync_plan.generated(root)

    def test_nine_finn_and_five_domain_gates_for_every_parent(self):
        for task in self.tasks:
            self.assertEqual(set(task["required_finn_gates"]), validate_package.FINN_GATES)
            self.assertEqual(set(task["required_domain_gates"]), validate_package.DOMAIN_GATES)
            self.assertFalse(task["completion_claim"])
            self.assertEqual(task["evidence_status"], "NOT_RUN")
            self.assertEqual(task["independent_review"], "NOT_RUN")
            self.assertEqual(task["human_contract_approval"], "NOT_GRANTED_BY_HANDOFF")
            self.assertEqual(task["human_merge"], "REQUIRED_NOT_AUTHORIZED_BY_HANDOFF")

    def test_budget_is_explicit_and_time_is_not_misrepresented_as_approved(self):
        for task in self.tasks:
            budget = task["budget"]
            self.assertEqual((budget["max_total_attempts"], budget["max_retries"]), (3, 2))
            self.assertEqual(budget["wall_clock_minutes_proposal"], 90)
            self.assertEqual(budget["wall_clock_approval"], "REQUIRES_OWNER_BEFORE_AGENT_READY")
            self.assertEqual(budget["paid_model_calls_without_approval"], 0)
            self.assertEqual(budget["external_effect_retries"], "INSPECT_REMOTE_FIRST")
            self.assertIn("not runtime enforcement", budget["attempt_limit_source"])

    def test_offline_card_retained_blocked_and_not_a_hidden_global_dependency(self):
        offline = self.by_id["PWA-3F"]
        self.assertEqual(offline["status"], "BLOCKED")
        self.assertTrue(offline["conditional"])
        self.assertTrue(all(task["status"] == "PROPOSED" for task in self.tasks if task["id"] != "PWA-3F"))
        self.assertFalse(any("PWA-3F" in task["depends_on"] for task in self.tasks))
        self.assertIn("owner-approved deferral", self.plan["conditional_completion"])
        self.assertEqual(self.plan["product_root"], "mp-app/studio/")
        self.assertEqual(self.plan["forbidden_second_product_root"], "mp-app/pwa-member/")

    def test_all_original_decisions_match_source_lines_not_reserved_placeholders(self):
        register = read_json("templates/DECISION_REGISTER.json")
        self.assertEqual([r["id"] for r in register["decisions"]], [f"D-{i:02d}" for i in range(1, 12)])
        source = (PAYLOAD / "references/docs__MuscleParadise__architecture__finn-loop-microtask-backlog-draft-v1-2026-11-23.md.source.txt").read_text().splitlines()
        self.assertEqual([r["source_line"] for r in register["decisions"]], list(range(68, 79)))
        for decision in register["decisions"]:
            original = [s.strip() for s in source[decision["source_line"] - 1].split("|")[1:-1]]
            self.assertEqual(original, [decision["id"], decision["title_fa"], decision["acceptance_fa"], decision["non_goals_fa"]])
            self.assertIsNone(decision["owner_response"])
            self.assertTrue(decision["original_text_recovered"])
            self.assertEqual(decision["status"], "DECISION")
            self.assertIn(PIN, decision["source_url"])
        known = {r["id"] for r in register["decisions"]}
        referenced = {d for t in self.tasks for d in t["owner_decisions"]}
        referenced |= {d["decision"] for d in self.plan["conditional_decision_dependencies"]}
        self.assertEqual(referenced, known)

    def test_traceability_is_exactly_one_to_one(self):
        with (PAYLOAD / "TASK_TRACEABILITY.csv").open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual([row["original_id"] for row in rows], IDS)
        for expected, row in zip(EXPECTED, rows):
            self.assertEqual((row["original_id"], row["original_title"]), expected)
            for field in ("plan_id", "handoff_heading", "diagram_id"):
                self.assertEqual(row[field], expected[0])
            self.assertEqual(row["check_status"], "STRUCTURAL_ONLY_NOT_PRODUCT_QA")

    def test_seventeen_features_mapped_to_real_ids_without_claiming_parity(self):
        inventory = read_json("references/MP_SOURCE_INVENTORY.json")
        with (PAYLOAD / "templates/FEATURE_PARITY.csv").open() as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 17)
        self.assertEqual({row["feature"] for row in rows}, set(preflight.FEATURES))
        self.assertEqual(set(inventory["features"]), set(preflight.FEATURES))
        for row in rows:
            self.assertTrue(set(row["pwa_ids"].split(";")).issubset(IDS))
            self.assertEqual((row["status"], row["evidence"], row["ownership"]), ("PROPOSED", "NOT_RUN", "UNKNOWN"))
        shop = next(row for row in rows if row["feature"] == "shop")
        self.assertIn("no checkout", shop["scope_note"])

    def test_source_paths_and_all_snapshots_have_pinned_provenance(self):
        inventory = read_json("references/MP_SOURCE_INVENTORY.json")
        self.assertEqual(inventory["commit"], PIN)
        self.assertTrue(inventory["source_only"])
        for task in self.tasks:
            for path in task["source_paths"]:
                self.assertTrue(inventory["verified_plan_source_paths"][path], path)
        snapshots = read_json("references/SOURCE_MANIFEST.json")
        self.assertEqual(len(snapshots), 27)
        for source in snapshots:
            self.assertEqual(source["commit"], PIN)
            self.assertIn(PIN, source["url"])
            self.assertEqual(hashlib.sha256((PAYLOAD / source["package_path"]).read_bytes()).hexdigest(), source["sha256"])
            self.assertEqual(source["status"], "STATIC_SOURCE_NOT_EXECUTED")

    def test_static_api_inventory_and_flutter_workflow_are_not_replaced(self):
        api = read_json("references/mp-api-routes.snapshot.json")
        self.assertEqual((len(api["paths"]), len(api["operations"])), (141, 163))
        with (PAYLOAD / "references/MP_API_OPERATIONS.csv").open() as stream:
            self.assertEqual(len(list(csv.DictReader(stream))), 163)
        web = (PAYLOAD / "references/.github__workflows__web.yml.source.txt").read_text()
        self.assertIn("flutter build web --release --base-href /", web)
        self.assertIn("mp-app/client/build/web", web)
        self.assertIn("PWA-05", IDS)
        self.assertIn("PWA-55", IDS)

    def test_child_templates_have_all_gates_and_human_review_merge_contract(self):
        for name in ("MICROTASK_TEMPLATE.fa.md", "EVIDENCE_TEMPLATE.fa.md"):
            content = (PAYLOAD / "templates" / name).read_text()
            self.assertTrue(validate_package.FINN_GATES.issubset(set(re.findall(r"G[1-9]-[a-z-]+", content))))
            for domain in validate_package.DOMAIN_GATES:
                self.assertRegex(content, r"\| " + domain + r" \|")
            self.assertIn("parent", content)
            self.assertIn("SHA", content)
            self.assertIn("review", content)
            self.assertIn("merge", content)
            self.assertIn("NOT_RUN", content)

    def test_mutation_removing_any_one_of_50_cards_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            temporary_payload(root)
            for task_id in IDS:
                with self.subTest(task=task_id):
                    plan = copy.deepcopy(self.plan)
                    plan["plan"] = [r for r in plan["plan"] if r["id"] != task_id]
                    (root / "PWA_PLAN.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
                    self.assertTrue(any("all 50 original IDs" in problem for problem in validate_package.validate_plan(root)))

    def test_mutation_changing_title_or_acceptance_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            temporary_payload(root)
            for key in ("title_fa", "source_acceptance_fa"):
                plan = copy.deepcopy(self.plan)
                plan["plan"][0][key] = "MUTATED_BOUNDARY_NOT_APPROVED"
                (root / "PWA_PLAN.json").write_text(json.dumps(plan))
                self.assertIn("Source field changed: PWA-00/" + key, validate_package.validate_plan(root))

    def test_mutation_inventing_owner_approval_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            temporary_payload(root)
            register = read_json("templates/DECISION_REGISTER.json")
            register["decisions"][0]["owner_response"] = "FAKE_APPROVAL"
            (root / "templates/DECISION_REGISTER.json").write_text(json.dumps(register))
            self.assertIn("Unrecovered or invented owner decision: D-01", validate_package.validate_plan(root))


class V2PreflightTests(unittest.TestCase):
    def test_wrong_checkout_is_blocked_with_no_product_qa_claim(self):
        result = preflight.inspect_repository(ROOT)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("mp-app" in p for p in result["problems"]))
        self.assertIn("independent_review", result["checks_not_executed"])
        self.assertIn("human_approval", result["checks_not_executed"])

    def test_fixture_only_two_manifests_read_no_subprocess_or_env_db(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            (root / ".env").write_text("DO_NOT_READ")
            (root / "member.db").write_text("DO_NOT_READ")
            with patch.object(preflight, "_safe_read", wraps=preflight._safe_read) as reader, patch.object(preflight.subprocess, "run", side_effect=AssertionError("No app commands")):
                result = preflight.inspect_layout(root)
            self.assertEqual(result["problems"], [])
            self.assertEqual(result["static_inventory"]["declared_operations"], 1)
            self.assertEqual({c.args[1] for c in reader.call_args_list}, {"mp-app/backend/api/routes.json", "mp-app/studio/package.json"})

    def test_successful_inventory_is_not_readiness_even_when_pin_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            with patch.object(preflight, "git_metadata", return_value={"verified_checkout": True, "head": PIN}):
                result = preflight.inspect_repository(root)
            self.assertEqual(result["status"], "INVENTORY_OK_NOT_QA")
            self.assertEqual(result["reference_relation"], "MATCHES_PIN_NOT_QA")
            self.assertIn("not AGENT-READY", result["warning"])

    def test_different_pin_requires_reconciliation_not_checkout_or_reset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            with patch.object(preflight, "git_metadata", return_value={"verified_checkout": True, "head": "a" * 40}):
                result = preflight.inspect_repository(root)
            self.assertEqual(result["status"], "INVENTORY_OK_NOT_QA")
            self.assertEqual(result["reference_relation"], "RECONCILE_CURRENT_SOURCE_DO_NOT_RESET_OR_SWITCH")

    def test_layout_without_git_root_remains_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            result = preflight.inspect_repository(root)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertFalse(result["git"]["verified_checkout"])

    def test_malformed_manifest_never_echoes_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            (root / "mp-app/backend/api/routes.json").write_text("NEVER_ECHO_MALFORMED_INPUT")
            result = preflight.inspect_layout(root)
            self.assertTrue(result["problems"])
            self.assertNotIn("NEVER_ECHO", json.dumps(result))

    def test_missing_or_extra_role_is_reconcile_not_automatic_grant(self):
        for roles in (["member"], sorted(preflight.KNOWN_ROLES | {"extra-role"})):
            with self.subTest(roles=roles), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                fixture(root)
                file = root / "mp-app/backend/api/routes.json"
                doc = json.loads(file.read_text())
                doc["operations"][0]["roles"] = roles
                file.write_text(json.dumps(doc))
                before = file.read_bytes()
                self.assertTrue(preflight.inspect_layout(root)["problems"])
                self.assertEqual(before, file.read_bytes())

    def test_manifest_symlink_outside_checkout_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other:
            root = Path(tmp)
            fixture(root)
            destination = Path(other) / "routes.json"
            destination.write_text("SHOULD_NOT_READ")
            file = root / "mp-app/backend/api/routes.json"
            file.unlink()
            file.symlink_to(destination)
            result = preflight.inspect_layout(root)
            self.assertTrue(any("outside selected checkout" in p for p in result["problems"]))
            self.assertNotIn("SHOULD_NOT_READ", json.dumps(result))

    def test_cli_wrong_checkout_exits_two(self):
        result = subprocess.run([sys.executable, str(PAYLOAD / "scripts/preflight.py"), "--repo", str(ROOT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "BLOCKED")


class V2PackageTests(unittest.TestCase):
    def test_tool_roots_are_exact_locked_private_and_have_no_lifecycle(self):
        for directory in ("node", "diagram"):
            base = PAYLOAD / "tooling" / directory
            package = json.loads((base / "package.json").read_text())
            lock = json.loads((base / "package-lock.json").read_text())
            self.assertTrue(package["private"])
            self.assertEqual(package["version"], "2.0.0")
            self.assertFalse(package.get("scripts"))
            for field in ("dependencies", "devDependencies"):
                expected = package.get(field, {})
                self.assertEqual(lock["packages"][""].get(field, {}), expected)
                for name, version in expected.items():
                    self.assertRegex(version, r"^\d+\.\d+\.\d+$")
                    self.assertEqual(lock["packages"]["node_modules/" + name]["version"], version)
            self.assertEqual(lock["packages"][""]["name"], package["name"])
        diagram = read_json("tooling/diagram/package.json")
        self.assertEqual(diagram["dependencies"], {"@viz-js/viz": "3.31.0", "sharp": "0.35.5"})

    def test_roadmap_sources_current_and_svg_has_each_task_node_once(self):
        for name, expected in make_roadmap.sources().items():
            self.assertEqual((PAYLOAD / "diagrams" / name).read_text(), expected)
        tree = ET.fromstring((PAYLOAD / "diagrams/PWA_50_Microloops.fa.svg").read_bytes())
        namespace = {"s": "http://www.w3.org/2000/svg"}
        titles = [node.text for node in tree.findall(".//s:g/s:title", namespace)]
        nodes = [name for name in titles if name and name.startswith("pwa_")]
        self.assertEqual(set(nodes), {"pwa_" + task_id[4:] for task_id in IDS})
        self.assertEqual(len(nodes), 50)

    def test_roadmap_phase_headers_are_top_aligned_and_ordered_regression(self):
        tree = ET.fromstring((PAYLOAD / "diagrams/PWA_50_Microloops.fa.svg").read_bytes())
        ns = {"s": "http://www.w3.org/2000/svg"}
        positions = {}
        for group in tree.findall(".//s:g", ns):
            title = group.find("s:title", ns)
            if title is not None and title.text and re.fullmatch(r"h[0-5]_[01]", title.text):
                labels = group.findall("s:text", ns)
                positions[title.text] = (sum(float(x.attrib["x"]) for x in labels) / len(labels), sum(float(x.attrib["y"]) for x in labels) / len(labels))
        order = ["h0_0", "h1_0", "h2_0", "h3_0", "h3_1", "h4_0", "h5_0"]
        self.assertEqual(set(positions), set(order))
        self.assertLess(max(positions[k][1] for k in order) - min(positions[k][1] for k in order), 0.2)
        xs = [positions[k][0] for k in order]
        self.assertEqual(xs, sorted(xs))

    def test_rendered_images_signatures_sizes_and_explicit_rtl(self):
        for stem, width in (("PWA_Finn_Loop_Flow.fa", 4200), ("PWA_50_Microloops.fa", 5200)):
            png = (PAYLOAD / "diagrams" / (stem + ".png")).read_bytes()
            self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
            w, h = struct.unpack(">II", png[16:24])
            self.assertEqual(w, width)
            self.assertGreater(h, 1200)
            self.assertLess(h, 5000)
            svg = (PAYLOAD / "diagrams" / (stem + ".svg")).read_text()
            self.assertIn('direction="rtl" unicode-bidi="embed"', svg)
            self.assertNotIn("<script", svg)

    def test_active_docs_copies_match_v2_but_v1_archive_is_unchanged(self):
        for stem in ("PWA_Finn_Loop_Flow.fa", "PWA_50_Microloops.fa"):
            for extension in ("dot", "mmd", "png", "svg"):
                name = stem + "." + extension
                self.assertEqual((ROOT / "docs" / name).read_bytes(), (PAYLOAD / "diagrams" / name).read_bytes())
        archive = BASE / "releases/MP-PWA-Arena-Handoff-v1.0.0.zip"
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), "019c3cefb570897fcebc0da82827d99301df28a90a41854f7ea7b4de790acff8")

    def test_offline_html_has_all_fifty_cards_two_embedded_images_and_no_scripts(self):
        class Parser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.images, self.ids, self.scripts, self.assets = [], [], [], []
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if "id" in attrs:
                    self.ids.append(attrs["id"])
                if tag == "img":
                    self.images.append(attrs.get("src", ""))
                if tag == "script":
                    self.scripts.append(attrs)
                if tag in {"iframe", "object", "link", "video", "audio"}:
                    self.assets.append((tag, attrs))
        content = (PAYLOAD / "HANDOFF.fa.html").read_text()
        parser = Parser()
        parser.feed(content)
        self.assertEqual(len(parser.images), 2)
        self.assertTrue(all(img.startswith("data:image/png;base64,") for img in parser.images))
        self.assertEqual(parser.scripts, [])
        self.assertEqual(parser.assets, [])
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        self.assertIn('lang="fa" dir="rtl"', content)
        self.assertIn("default-src 'none'", content)
        self.assertEqual(len(re.findall(r"<h3[^>]*>PWA-[0-9A-F]{2} — ", content)), 50)
        for task_id, title in EXPECTED:
            self.assertIn(task_id + " — " + title, content)
        for source in ("FINN_LOOP_FINAL.fa.md", "TOOLCHAIN.fa.md", "DECISION_PACKAGE.fa.md", "MICROLOOPS.fa.md"):
            self.assertIn('data-source="' + source + '"', content)

    def test_document_smoke_report_is_bound_to_this_html_not_the_product(self):
        report = read_json("references/HANDOFF_HTML_SMOKE.json")
        self.assertEqual(report["document_sha256"], hashlib.sha256((PAYLOAD / "HANDOFF.fa.html").read_bytes()).hexdigest())
        self.assertEqual(report["recipe_sha256"], hashlib.sha256((PAYLOAD / "references/HANDOFF_HTML_SMOKE.recipe.mjs.txt").read_bytes()).hexdigest())
        self.assertEqual(report["status"], "PASS_DOCUMENT_ONLY_NOT_PRODUCT_QA")
        self.assertIn("NOT MP app", report["scope"])
        self.assertEqual((report["external_request_count"], report["page_error_count"]), (0, 0))
        self.assertEqual([r["viewport"]["width"] for r in report["results"]], [1280, 390, 320])
        for row in report["results"]:
            self.assertEqual(row["status"], "PASS_DOCUMENT_ONLY")
            self.assertEqual(row["taskHeadings"], 50)
            self.assertEqual(row["scrollWidth"], row["width"])
            self.assertEqual(row["ownScripts"], 0)
            self.assertTrue(row["uniqueAnchors"])
            self.assertEqual(row["direction"], "rtl")

    def test_local_markdown_links_resolve_and_no_template_markers_in_main(self):
        for file in builder.payload_files():
            if file.suffix != ".md":
                continue
            content = re.sub(r"```.*?```", "", file.read_text(), flags=re.S)
            for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", content):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                self.assertTrue((file.parent / target.split("#")[0]).exists(), str(file.relative_to(PAYLOAD)) + " -> " + target)
        self.assertNotRegex((PAYLOAD / "HANDOFF.fa.md").read_text(), r"\{\{[A-Z_]+\}\}")

    def test_every_payload_text_is_free_of_credential_signatures_and_runtime_artifacts(self):
        forbidden = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}")
        for file in builder.payload_files():
            self.assertNotIn("node_modules", file.parts)
            self.assertNotIn(file.suffix.lower(), {".db", ".sqlite", ".apk", ".exe", ".key", ".pem"})
            if file.suffix.lower() in {".md", ".txt", ".json", ".py", ".mjs", ".html", ".yml", ".cjs", ".csv"}:
                self.assertIsNone(forbidden.search(file.read_text()), str(file.relative_to(PAYLOAD)))

    def test_python_sources_compile_without_executing_application(self):
        for path in [BASE / "build_pwa_handoff.py", *list((PAYLOAD / "scripts").glob("*.py"))]:
            compile(path.read_text(), str(path), "exec")

    def test_portable_integrity_and_plan_validator(self):
        self.assertEqual(validate_package.validate_plan(), [])
        self.assertEqual(validate_package.validate_integrity(), [])
        result = subprocess.run([sys.executable, str(PAYLOAD / "scripts/validate_package.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "PACKAGE_OK_NOT_QA")

    def test_manifest_paths_cannot_escape_or_follow_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other:
            root = Path(tmp)
            for unsafe in ("../outside", "/absolute", "a/../../outside", "a\\outside", "./a", "C:/outside"):
                with self.subTest(path=unsafe), self.assertRaises(ValueError):
                    validate_package.safe_file(root, unsafe)
            (root / "link").symlink_to(Path(other), target_is_directory=True)
            with self.assertRaises(ValueError):
                validate_package.safe_file(root, "link/private.txt")

    def test_internal_manifests_cover_exactly_all_files_and_are_not_product_approval(self):
        manifest = read_json("PACKAGE_MANIFEST.json")
        self.assertEqual(manifest["task_count"], 50)
        self.assertEqual(manifest["product_source_snapshot"], PIN)
        expected = {f.relative_to(PAYLOAD).as_posix() for f in builder.payload_files(include_manifests=False)}
        self.assertEqual(expected, {row["path"] for row in manifest["files"]})
        for row in manifest["files"]:
            data = (PAYLOAD / row["path"]).read_bytes()
            self.assertEqual((len(data), hashlib.sha256(data).hexdigest()), (row["bytes"], row["sha256"]))

    def test_zip_crc_members_timestamp_permissions_contents_and_checksum(self):
        archive = BASE / "releases" / (builder.NAME + ".zip")
        expected = {builder.NAME + "/" + file.relative_to(PAYLOAD).as_posix(): file.read_bytes() for file in builder.payload_files()}
        with zipfile.ZipFile(archive) as bundle:
            self.assertIsNone(bundle.testzip())
            self.assertEqual(set(bundle.namelist()), set(expected))
            self.assertEqual(len(bundle.namelist()), len(expected))
            for member in bundle.infolist():
                self.assertNotIn("..", Path(member.filename).parts)
                self.assertFalse(member.filename.startswith("/"))
                self.assertEqual(member.date_time, builder.FIXED_ZIP_TIME)
                self.assertEqual(member.external_attr >> 16, 0o100644)
                self.assertEqual(bundle.read(member), expected[member.filename])
        self.assertEqual((BASE / "releases" / (builder.NAME + ".zip.sha256")).read_text().split()[0], hashlib.sha256(archive.read_bytes()).hexdigest())

    def test_extracted_zip_validates_without_delivery_repo_or_node_dependencies(self):
        archive = BASE / "releases" / (builder.NAME + ".zip")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with zipfile.ZipFile(archive) as bundle:
                bundle.extractall(root)
            extracted = root / builder.NAME
            self.assertFalse((extracted / "mp-app").exists())
            self.assertFalse((extracted / ".git").exists())
            for script in ("sync_plan.py", "make_roadmap.py", "validate_package.py"):
                argv = [sys.executable, str(extracted / "scripts" / script)]
                if script != "validate_package.py":
                    argv.append("--check")
                result = subprocess.run(argv, cwd=extracted, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, script + ": " + result.stdout + result.stderr)

    def test_zip_is_byte_reproducible_and_v1_cannot_be_regenerated(self):
        archive = BASE / "releases" / (builder.NAME + ".zip")
        before = archive.read_bytes()
        builder.build_zip()
        self.assertEqual(before, archive.read_bytes())
        legacy = builder_module.Bundle("1.0.0")
        with self.assertRaisesRegex(ValueError, "frozen"):
            legacy.render_html()
        with self.assertRaisesRegex(ValueError, "frozen"):
            legacy.write_manifests()
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            legacy.PAYLOAD = sandbox / "changed-payload"
            legacy.PAYLOAD.mkdir()
            legacy.RELEASES = sandbox
            original = sandbox / (legacy.NAME + ".zip")
            original.write_bytes(b"DO_NOT_OVERWRITE_FROZEN_ARCHIVE")
            with self.assertRaisesRegex(ValueError, "frozen"):
                legacy.build_zip()
            self.assertEqual(original.read_bytes(), b"DO_NOT_OVERWRITE_FROZEN_ARCHIVE")
        self.assertEqual(builder_module.Bundle().version, "2.0.0")


if __name__ == "__main__":
    unittest.main()
