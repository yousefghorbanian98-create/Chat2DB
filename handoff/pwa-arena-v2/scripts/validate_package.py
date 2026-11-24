#!/usr/bin/env python3
"""Read-only integrity + exact-source coverage checks for this handoff only.

Does not install tools, execute app/tests, access network/Git/DB, or approve
owners/reviews/releases. Exit 0 means PACKAGE_OK_NOT_QA; any problem exits 2.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re

from sync_plan import EXPECTED_IDS, generated, read_source

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {"node_modules", "__pycache__", ".cache", ".venv", ".git", "downloads"}
MANIFESTS = {"PACKAGE_MANIFEST.json", "MANIFEST.sha256"}
FINN_GATES = {"G1-spec", "G2-isolation", "G3-tool-scope", "G4-tests-security", "G5-branch-protection", "G6-evidence", "G7-human-approval", "G8-budget", "G9-adversarial-review"}
DOMAIN_GATES = {"security", "privacy", "finance", "legal", "product"}


def files(root: Path = ROOT, *, include_manifests: bool = True) -> list[Path]:
    result = []
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_PARTS or part.startswith('.venv-') for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError('Symlink not allowed in payload: ' + rel.as_posix())
        if path.is_file() and (include_manifests or rel.as_posix() not in MANIFESTS):
            result.append(path)
    return result


def safe_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or '\\' in relative or ':' in relative:
        raise ValueError('Unsafe manifest path')
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts or str(path) != relative:
        raise ValueError('Unsafe manifest path')
    candidate = root.joinpath(*path.parts)
    current = candidate
    while current != root:
        if current.is_symlink():
            raise ValueError('Manifest path follows a symlink')
        current = current.parent
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError('Manifest path is outside package')
    return candidate


def validate_plan(root: Path = ROOT) -> list[str]:
    problems = []
    rows = read_source(root)
    plan = json.loads((root / 'PWA_PLAN.json').read_text(encoding='utf-8'))
    tasks = plan.get('plan', [])
    if [r.get('id') for r in tasks] != list(EXPECTED_IDS) or plan.get('task_count') != 50:
        problems.append('PWA_PLAN must preserve all 50 original IDs in source order')
    if plan.get('product_root') != 'mp-app/studio/':
        problems.append('Studio must remain the single React product root')
    if plan.get('phase_counts') != [6, 8, 5, 16, 8, 7]:
        problems.append('Phase counts do not match the user inventory')
    for source, task in zip(rows, tasks):
        for key in ('id', 'phase', 'title_fa', 'source_acceptance_fa'):
            if source[key] != task.get(key):
                problems.append('Source field changed: ' + source['id'] + '/' + key)
        if task.get('acceptance_fa') != [source['source_acceptance_fa']]:
            problems.append('Source acceptance changed: ' + source['id'])
        if set(task.get('required_finn_gates', [])) != FINN_GATES or set(task.get('required_domain_gates', [])) != DOMAIN_GATES:
            problems.append('Missing per-task Finn/domain gate: ' + source['id'])
        if task.get('completion_claim') is not False or task.get('evidence_status') != 'NOT_RUN':
            problems.append('Unexpected product completion/evidence claim: ' + source['id'])
        expected_status = 'BLOCKED' if source['id'] == 'PWA-3F' else 'PROPOSED'
        if task.get('status') != expected_status:
            problems.append('Unexpected initial execution status: ' + source['id'])
        budget = task.get('budget', {})
        if budget.get('max_total_attempts') != 3 or budget.get('max_retries') != 2 or budget.get('paid_model_calls_without_approval') != 0:
            problems.append('Unexpected attempt/cost budget: ' + source['id'])
        if budget.get('wall_clock_approval') != 'REQUIRES_OWNER_BEFORE_AGENT_READY':
            problems.append('Unapproved time budget cannot be treated as approved: ' + source['id'])
    for name, expected in generated(root).items():
        if (root / name).read_text(encoding='utf-8') != expected:
            problems.append('Generated plan artifact out of sync: ' + name)
    with (root / 'TASK_TRACEABILITY.csv').open(encoding='utf-8') as stream:
        traces = list(csv.DictReader(stream))
    if [r['original_id'] for r in traces] != list(EXPECTED_IDS):
        problems.append('Source traceability must be 1:1 for all 50 IDs')
    else:
        for source, row in zip(rows, traces):
            if any(row[key] != source['id'] for key in ('plan_id', 'handoff_heading', 'diagram_id')) or row['original_title'] != source['title_fa']:
                problems.append('Traceability field changed: ' + source['id'])
    roadmap = (root / 'diagrams/PWA_50_Microloops.fa.mmd').read_text(encoding='utf-8')
    for row in rows:
        if row['id'] + ' — ' + row['title_fa'] not in roadmap:
            problems.append('Roadmap missing original title: ' + row['id'])
    dot = (root / 'diagrams/PWA_50_Microloops.fa.dot').read_text(encoding='utf-8')
    svg = (root / 'diagrams/PWA_50_Microloops.fa.svg').read_text(encoding='utf-8')
    for label, content in [('DOT', dot), ('SVG', svg)]:
        # Graphviz XML-escapes hyphens as &#45;; compare decoded text, not bytes.
        found = set(re.findall(r'PWA-[0-9A-F]{2}(?![0-9A-Za-z])', html.unescape(content)))
        if found != set(EXPECTED_IDS):
            problems.append('Roadmap ' + label + ' ID coverage mismatch')
    register = json.loads((root / 'templates/DECISION_REGISTER.json').read_text(encoding='utf-8'))
    if [r.get('id') for r in register['decisions']] != [f'D-{i:02d}' for i in range(1, 12)]:
        problems.append('All original D-01 through D-11 must be recovered')
    decision_source = (root / 'references/docs__MuscleParadise__architecture__finn-loop-microtask-backlog-draft-v1-2026-11-23.md.source.txt').read_text(encoding='utf-8').splitlines()
    for decision in register['decisions']:
        if not decision.get('original_text_recovered') or decision.get('owner_response') is not None:
            problems.append('Unrecovered or invented owner decision: ' + decision.get('id', '?'))
        line = decision_source[decision['source_line'] - 1]
        original = [value.strip() for value in line.split('|')[1:-1]]
        if original != [decision['id'], decision['title_fa'], decision['acceptance_fa'], decision['non_goals_fa']]:
            problems.append('Original D definition changed: ' + decision['id'])
    return problems


def validate_integrity(root: Path = ROOT) -> list[str]:
    problems = []
    manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    expected = {f.relative_to(root).as_posix() for f in files(root, include_manifests=False)}
    names = [r['path'] for r in manifest['files']]
    if len(names) != len(set(names)) or set(names) != expected:
        problems.append('Package manifest inventory mismatch or duplicate')
    for row in manifest['files']:
        data = safe_file(root, row['path']).read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            problems.append('Package manifest digest mismatch: ' + row['path'])
    seen = set()
    for line in (root / 'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        if name in seen:
            problems.append('Duplicate checksum entry: ' + name)
        seen.add(name)
        if not re.fullmatch('[0-9a-f]{64}', digest) or hashlib.sha256(safe_file(root, name).read_bytes()).hexdigest() != digest:
            problems.append('Checksum mismatch: ' + name)
    expected_checks = {f.relative_to(root).as_posix() for f in files(root) if f.name != 'MANIFEST.sha256'}
    if seen != expected_checks:
        problems.append('Checksum inventory mismatch')
    for source in json.loads((root / 'references/SOURCE_MANIFEST.json').read_text(encoding='utf-8')):
        data = safe_file(root, source['package_path']).read_bytes()
        if hashlib.sha256(data).hexdigest() != source['sha256'] or source['commit'] not in source['url']:
            problems.append('Source provenance mismatch: ' + source['path'])
    return problems


def main() -> int:
    try:
        problems = validate_plan() + validate_integrity()
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        # Avoid echoing arbitrary source/secret contents from malformed inputs.
        problems = ['Cannot safely validate package: ' + type(error).__name__]
    print(json.dumps({
        'status': 'BLOCKED' if problems else 'PACKAGE_OK_NOT_QA',
        'scope': 'Handoff integrity and exact 50-row source coverage only; no application checks or approvals',
        'problems': problems,
    }, ensure_ascii=False, indent=2))
    return 2 if problems else 0


if __name__ == '__main__':
    raise SystemExit(main())
