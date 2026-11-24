#!/usr/bin/env python3
"""Generate DOT + Mermaid roadmap from the preserved 50 source rows only.

--check compares text without writing; image rendering is a separate explicit step.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import textwrap

from sync_plan import PHASE_TITLES, read_source

ROOT = Path(__file__).resolve().parents[1]


def sources(root: Path = ROOT) -> dict[str, str]:
    rows = read_source(root)
    q = lambda value: json.dumps(value, ensure_ascii=False)
    dot = [
        'digraph PWA50 {',
        'graph [rankdir=TB, newrank=true, bgcolor="#f7fafc", pad="0.45", nodesep="0.24", ranksep="0.30", fontname="DejaVu Sans", fontsize=28, labelloc=t, label="MUSCLE PARADISE · PWA 2.0.0 · 2026-11-24\\n۵۰ میکرولوپ با شناسه و عنوان اصلی؛ همه پیشنهادی، نه شاهد اجرای محصول\\nStudio React مشترک؛ Flutter/Android و Electron محفوظ"]',
        'node [shape=box, style="rounded,filled", color="#80a8b8", fillcolor="#edf6fc", fontcolor="#163244", fontname="DejaVu Sans", fontsize=18, margin="0.20,0.14", width=3.6]',
        'edge [color="#9cb3bf", arrowsize=0.7]',
    ]
    mermaid = ['flowchart TB', '  %% All 50 user-supplied parent IDs. Edges between phase headers are orientation, not the exact DAG.']
    headers = []
    for phase in range(6):
        current = [r for r in rows if r['phase'] == phase]
        dot += [f'subgraph cluster_phase{phase} {{', 'style="rounded,filled"; color="#b7cad4"; fillcolor="#ffffff";', f'label={q(f"فاز {phase} · {len(current)} کارت")}; fontsize=22;']
        mermaid += [f'  subgraph phase{phase}["فاز {phase} · {len(current)} کارت · {PHASE_TITLES[phase]}"]', '    direction TB']
        lanes = [current[:8], current[8:]] if phase == 3 else [current]
        for lane_num, lane in enumerate(lanes):
            h = f'h{phase}_{lane_num}'
            headers.append(h)
            title = PHASE_TITLES[phase] if not lane_num else 'ادامهٔ تجربه‌های عضو'
            title = '\n'.join(textwrap.wrap(title, width=28))
            dot += [f'{h} [label={q(title)}, fillcolor="#123e50", fontcolor="#ffffff", color="#123e50", fontsize=19]']
            previous = h
            for row in lane:
                task_id = row['id']
                label = task_id + '\n' + '\n'.join(textwrap.wrap(row['title_fa'], width=30, break_long_words=False))
                if task_id == 'PWA-3F':
                    label += '\nCONDITIONAL · BLOCKED'
                attrs = ', fillcolor="#fff0d7", color="#d58a25"' if task_id == 'PWA-3F' else ''
                n = 'pwa_' + task_id[4:]
                dot += [f'{n} [label={q(label)}{attrs}]', f'{previous} -> {n} [style=invis, weight=8]']
                mermaid += [f'    {n}[{q(task_id + " — " + row["title_fa"])}]']
                previous = n
        dot += ['}']
        mermaid += ['  end']
    dot += ['{ rank=same; ' + '; '.join(headers) + '; }']
    for left, right in zip(headers, headers[1:]):
        dot += [f'{left} -> {right} [style=invis, weight=15]']
    dot += ['legend [shape=note, fillcolor="#ffffff", label="آبی: PROPOSED / NOT_RUN · نارنجی: آفلاین فقط با تصویب\\nترتیب فازها راهنماست؛ DAG و تصمیم‌ها در PWA_PLAN.json\\n۹ حوزهٔ Finn + ۵ گیت دامنه‌ای برای هر کارت و فرزند؛ review/merge انسانی\\nPWA-3F حذف نشده؛ defer فقط با تصمیم صریح مالک، نه PASS"]', 'pwa_56 -> legend [style=invis]', '}']
    mermaid += ['  phase0 -.-> phase1 -.-> phase2 -.-> phase3 -.-> phase4 -.-> phase5', '  classDef conditional fill:#fff0d7,stroke:#d58a25,color:#163244;', '  class pwa_3F conditional;', '  %% PWA-3F BLOCKED until explicit offline security/sync/conflict approval; never silently omitted.']
    return {'PWA_50_Microloops.fa.dot': '\n'.join(dot) + '\n', 'PWA_50_Microloops.fa.mmd': '\n'.join(mermaid) + '\n'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for name, content in sources().items():
        path = ROOT / 'diagrams' / name
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                stale.append(name)
        else:
            path.write_text(content, encoding='utf-8')
    if stale:
        print('OUT_OF_SYNC: ' + ', '.join(stale))
        return 1
    print('Roadmap source: 50 preserved parent IDs; not application evidence')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
