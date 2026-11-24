#!/usr/bin/env python3
"""Versioned deterministic documentation ZIP builder; never executes MP code.

Default: build v2.0.0. v1.0.0 is frozen: only its archived bytes can be repacked.
Prerequisite: isolated `pip install -r handoff/requirements-docs.txt` for v2 HTML.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
FIXED_ZIP_TIME = (2026, 11, 24, 0, 0, 0)
MANIFESTS = {"PACKAGE_MANIFEST.json", "MANIFEST.sha256"}
EXCLUDED_PARTS = {"node_modules", "__pycache__", ".cache", ".venv", ".git", "downloads"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Bundle:
    FIXED_ZIP_TIME = FIXED_ZIP_TIME

    def __init__(self, version: str = "2.0.0") -> None:
        if version not in {"1.0.0", "2.0.0"}:
            raise ValueError("Unknown handoff version")
        self.version = version
        self.PAYLOAD = HERE / ("pwa-arena-v1" if version == "1.0.0" else "pwa-arena-v2")
        self.RELEASES = HERE / "releases"
        self.NAME = "MP-PWA-Arena-Handoff-v" + version

    def payload_files(self, *, include_manifests: bool = True) -> list[Path]:
        files: list[Path] = []
        for candidate in sorted(self.PAYLOAD.rglob("*")):
            relative = candidate.relative_to(self.PAYLOAD)
            if any(part in EXCLUDED_PARTS or part.startswith(".venv-") for part in relative.parts):
                continue
            if candidate.is_symlink():
                raise ValueError("Symlink not allowed in portable handoff: " + str(relative))
            if not candidate.is_file():
                continue
            if not include_manifests and relative.as_posix() in MANIFESTS:
                continue
            if candidate.suffix.lower() in {".db", ".sqlite", ".sqlite3", ".apk", ".exe", ".pem", ".key", ".mp4"} or candidate.name.startswith(".env"):
                raise ValueError("Unexpected runtime/private artifact: " + str(relative))
            files.append(candidate)
        return files

    def render_html(self) -> None:
        if self.version == "1.0.0":
            raise ValueError("v1 payload is frozen; do not regenerate its HTML or manifests")
        try:
            import markdown
        except ImportError as exc:
            raise SystemExit("Install only the isolated docs dependency in handoff/requirements-docs.txt first") from exc
        sections = [
            ("guide", "HANDOFF.fa.md", "راهنمای شروع"),
            ("microloops", "MICROLOOPS.fa.md", "تمام ۵۰ میکرولوپ"),
            ("finn", "FINN_LOOP_FINAL.fa.md", "Finn نهایی"),
            ("decisions", "DECISION_PACKAGE.fa.md", "بستهٔ تصمیم"),
            ("tools", "TOOLCHAIN.fa.md", "نصب و کاربرد ابزار"),
            ("comparison", "COMPARISON_AND_CHANGELOG.fa.md", "مقایسه و اصلاحات"),
            ("verification", "VERIFICATION.fa.md", "مرز اعتبارسنجی"),
        ]
        parts = []
        for section_id, filename, _ in sections:
            source = (self.PAYLOAD / filename).read_text(encoding="utf-8")
            rendered = markdown.markdown(source, extensions=["tables", "fenced_code", "toc", "sane_lists"], output_format="html")
            # Markdown documents have overlapping heading slugs. Prefix every
            # internal anchor before combining them into one accessible page.
            rendered = re.sub(r'id="([^"]+)"', lambda match: 'id="' + section_id + '--' + match[1] + '"', rendered)
            rendered = re.sub(r'href="#([^"]+)"', lambda match: 'href="#' + section_id + '--' + match[1] + '"', rendered)
            for target_id, target_file, _ in sections:
                rendered = rendered.replace('href="' + target_file + '"', 'href="#' + target_id + '"')
            # Only the two explicitly owned PNGs are embedded; no external resources.
            def image(match: re.Match) -> str:
                relative = match.group(1)
                allowed = {"diagrams/PWA_Finn_Loop_Flow.fa.png", "diagrams/PWA_50_Microloops.fa.png"}
                if relative not in allowed:
                    raise ValueError("Unexpected HTML image source")
                data = (self.PAYLOAD / relative).read_bytes()
                return 'src="data:image/png;base64,' + base64.b64encode(data).decode("ascii") + '"'
            rendered = re.sub(r'src="([^"]+)"', image, rendered)
            parts.append('<section id="' + section_id + '" data-source="' + html.escape(filename) + '">' + rendered + '</section>')
        navigation = " · ".join('<a href="#' + section_id + '">' + title + '</a>' for section_id, _, title in sections)
        document = """<!doctype html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Muscle Paradise — تحویل کامل PWA و Finn · 2.0.0</title>
<style>
:root{color-scheme:light;--ink:#172d3c;--muted:#536977;--accent:#087a66;--line:#d4e2e5}
*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;background:#f0f5f6;color:var(--ink);font:16px/2 Tahoma,'DejaVu Sans',Arial,sans-serif}
main{max-width:1140px;margin:30px auto;background:white;padding:clamp(18px,5vw,58px);border:1px solid var(--line);border-radius:16px;min-width:0}
.banner{background:#123e50;color:#edfffb;border-radius:12px;padding:24px 26px;margin-bottom:22px}.banner small{display:block;color:#bddde8;direction:ltr;text-align:right;font-size:12px}.banner strong{font-size:25px;display:block;margin:8px 0}.banner p{margin:0;color:#d4efe9}
nav{padding:14px 16px;background:#eef6f6;border-radius:9px}nav a{white-space:normal}section+section{border-top:6px solid var(--line);margin-top:60px;padding-top:28px}
h1{font-size:27px;line-height:1.8}h2{font-size:22px;margin:46px 0 16px;padding-bottom:8px;border-bottom:2px solid var(--line)}h3{font-size:19px;margin-top:30px}a{color:#006caa;text-underline-offset:3px;overflow-wrap:anywhere}
p,li,td,th,h1,h2,h3{overflow-wrap:anywhere}blockquote{margin:18px 0;border-right:4px solid var(--accent);background:#f0f8f6;padding:10px 18px;border-radius:7px}
code{font:13px/1.8 Consolas,'DejaVu Sans Mono',monospace;direction:ltr;unicode-bidi:isolate;background:#edf3f5;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}
pre{direction:ltr;text-align:left;overflow:auto;max-width:100%;background:#112c37;color:#e0f4f1;border-radius:10px;padding:18px;line-height:1.8}pre code{background:transparent;color:inherit;padding:0;white-space:pre;overflow-wrap:normal}
table{border-collapse:collapse;width:100%;max-width:100%;margin:20px 0;font-size:14px;display:block;overflow:auto}th,td{border:1px solid var(--line);padding:9px 11px;text-align:right;vertical-align:top}th{background:#eaf4f2}tr:nth-child(even){background:#f8fafb}
img{display:block;max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px;margin:22px auto}hr{border:0;border-top:1px solid var(--line);margin:32px 0}footer{border-top:1px solid var(--line);padding-top:18px;margin-top:42px;color:var(--muted);font-size:13px}
@media(max-width:600px){main{margin:0;border:0;border-radius:0}.banner{padding:18px}.banner strong{font-size:21px}h1{font-size:23px}}
@media print{body{background:white}main{border:0;margin:0;max-width:none;padding:9mm}.banner{background:white;color:black;border:1px solid #777}.banner small,.banner p{color:black}pre{white-space:pre-wrap;background:#eee;color:black}table{font-size:10px}a{color:black}h2,h3{break-after:avoid}}
</style></head><body><main>
<header class="banner"><small>ARENA · MUSCLE PARADISE · HANDOFF 2.0.0 · 2026-11-24</small>
<strong>از PWA-00؛ Studio را گسترش بده، اپ دوم نساز.</strong>
<p>۵۰ شناسه و مرز پذیرش اصلی · یک PWA عضو/کادر · Flutter/Android محفوظ · برنامه، نه QA محصول</p></header>
""" + "<nav aria-label=\"بخش‌های تحویل\">" + navigation + "</nav>" + "\n".join(parts) + """
<footer>خواندن این HTML به شبکه، فونت بیرونی، اسکریپت یا tracker نیاز ندارد. دو تصویر، همهٔ ۵۰ کارت، Finn، تصمیم‌ها و راهنمای ابزارها تعبیه شده‌اند. سایر templateها/sourceها در همان ZIP هستند؛ پیوندهای بیرونی فقط هنگام انتخاب کاربر شبکه می‌خواهند. این فایل گواه آمادگی محصول یا مجوز انتشار نیست.</footer>
</main></body></html>
"""
        (self.PAYLOAD / "HANDOFF.fa.html").write_text(document, encoding="utf-8")

    def write_manifests(self) -> None:
        if self.version == "1.0.0":
            raise ValueError("v1 manifests are frozen")
        records = []
        for file in self.payload_files(include_manifests=False):
            data = file.read_bytes()
            records.append({"path": file.relative_to(self.PAYLOAD).as_posix(), "bytes": len(data), "sha256": digest(data)})
        manifest = {
            "name": self.NAME, "version": self.version, "date_utc": "2026-11-24",
            "purpose": "Documentation handoff, not implemented PWA, independent review or product release",
            "task_count": 50, "phase_counts": [6, 8, 5, 16, 8, 7],
            "source_inventory": "SOURCE_PLAN.fa.md",
            "product_source_snapshot": "c46e792657e361cd09799c896c47149b4a5c4d86",
            "product_source_reference_branch": "arena/5e0f64cf-mp",
            "delivery_base_commit": "ded065ebaa4cb9430338889cdea3b0ed1ad57836",
            "supersedes_handoff_delivery_commit": "be46f1c8773f249db75665eefd6d0c0db478a325",
            "excluded_from_this_manifest_to_avoid_self_reference": sorted(MANIFESTS),
            "files": records,
        }
        (self.PAYLOAD / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        checksums = []
        for file in self.payload_files():
            if file.name != "MANIFEST.sha256":
                checksums.append(digest(file.read_bytes()) + "  " + file.relative_to(self.PAYLOAD).as_posix())
        (self.PAYLOAD / "MANIFEST.sha256").write_text("\n".join(checksums) + "\n", encoding="utf-8")

    def build_zip(self) -> Path:
        self.RELEASES.mkdir(exist_ok=True)
        archive = self.RELEASES / (self.NAME + ".zip")
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for file in self.payload_files():
                info = zipfile.ZipInfo(self.NAME + "/" + file.relative_to(self.PAYLOAD).as_posix(), date_time=FIXED_ZIP_TIME)
                info.create_system = 3
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        data = buffer.getvalue()
        checksum = digest(data)
        if self.version == "1.0.0" and checksum != "019c3cefb570897fcebc0da82827d99301df28a90a41854f7ea7b4de790acff8":
            # Validate before touching the published historical archive. A
            # changed payload or compressor must not silently replace v1.
            raise ValueError("v1 is frozen: repacked bytes differ from the original published artifact")
        with zipfile.ZipFile(io.BytesIO(data)) as bundle:
            bad = bundle.testzip()
            if bad:
                raise ValueError("Corrupt ZIP member: " + bad)
        archive.write_bytes(data)
        (self.RELEASES / (self.NAME + ".zip.sha256")).write_text(checksum + "  " + archive.name + "\n", encoding="utf-8")
        return archive


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", choices=("1.0.0", "2.0.0"), default="2.0.0")
    args = parser.parse_args()
    bundle = Bundle(args.version)
    if args.version == "2.0.0":
        for script in ("sync_plan.py", "make_roadmap.py"):
            subprocess.run([sys.executable, str(bundle.PAYLOAD / "scripts" / script), "--check"], check=True)
        bundle.render_html()
        bundle.write_manifests()
        subprocess.run([sys.executable, str(bundle.PAYLOAD / "scripts/validate_package.py")], check=True)
    archive = bundle.build_zip()
    print(f"Built {archive.relative_to(HERE.parent)} ({archive.stat().st_size:,} bytes)")
    print("SHA-256 " + digest(archive.read_bytes()))
    print("Packaging only, not application behavior, independent review or owner approval.")


if __name__ == "__main__":
    main()
