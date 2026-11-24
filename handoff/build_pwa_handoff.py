#!/usr/bin/env python3
"""Build the requested, deterministic documentation ZIP (no source/install/deploy).

Build prerequisite, in an isolated documentation venv:
    python -m pip install -r handoff/requirements-docs.txt
Then, from repository root:
    python handoff/build_pwa_handoff.py
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
PAYLOAD = HERE / "pwa-arena-v1"
RELEASES = HERE / "releases"
NAME = "MP-PWA-Arena-Handoff-v1.0.0"
FIXED_ZIP_TIME = (2026, 11, 24, 0, 0, 0)
MANIFESTS = {"PACKAGE_MANIFEST.json", "MANIFEST.sha256"}
EXCLUDED_PARTS = {"node_modules", "__pycache__", ".cache", ".venv", ".git", "downloads"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def payload_files(*, include_manifests: bool = True) -> list[Path]:
    files: list[Path] = []
    for candidate in sorted(PAYLOAD.rglob("*")):
        relative = candidate.relative_to(PAYLOAD)
        if any(part in EXCLUDED_PARTS or part.startswith(".venv-") for part in relative.parts):
            continue
        if candidate.is_symlink():
            raise ValueError("Symlink not allowed in the portable handoff: " + str(relative))
        if not candidate.is_file():
            continue
        if not include_manifests and relative.as_posix() in MANIFESTS:
            continue
        if candidate.suffix.lower() in {".db", ".sqlite", ".sqlite3", ".apk", ".exe", ".pem", ".key", ".mp4"} or candidate.name.startswith(".env"):
            raise ValueError("Unexpected runtime/private artifact in handoff: " + str(relative))
        files.append(candidate)
    return files


def render_html() -> None:
    try:
        import markdown
    except ImportError as exc:
        raise SystemExit("Install only the isolated docs dependency in handoff/requirements-docs.txt first") from exc
    source = (PAYLOAD / "HANDOFF.fa.md").read_text(encoding="utf-8")
    content = markdown.markdown(source, extensions=["tables", "fenced_code", "toc", "sane_lists"], output_format="html")
    image = PAYLOAD / "diagrams/PWA_Finn_Loop_Flow.fa.png"
    embedded = "data:image/png;base64," + base64.b64encode(image.read_bytes()).decode("ascii")
    content = content.replace('src="diagrams/PWA_Finn_Loop_Flow.fa.png"', f'src="{embedded}"')
    document = """<!doctype html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>Muscle Paradise — تحویل Arena و PWA</title>
<style>
:root{color-scheme:light;--ink:#172d3c;--muted:#536977;--accent:#087a66;--line:#d4e2e5}
*{box-sizing:border-box}body{margin:0;background:#f0f5f6;color:var(--ink);font:16px/2 Tahoma,'DejaVu Sans',Arial,sans-serif}
main{max-width:1140px;margin:36px auto;background:white;padding:clamp(22px,5vw,64px);border:1px solid var(--line);border-radius:18px}
.banner{background:#073c3a;color:#edfffb;border-radius:12px;padding:26px 30px;margin-bottom:38px}
.banner small{display:block;color:#b6e2d8;letter-spacing:.04em;direction:ltr;text-align:right}.banner strong{font-size:25px;display:block;margin:8px 0}
.banner p{margin:0;color:#d4efe9}h1{font-size:29px;line-height:1.8}h2{font-size:23px;margin:54px 0 18px;padding-bottom:9px;border-bottom:2px solid var(--line)}
h3{font-size:19px;margin-top:32px}h4{font-size:18px;color:var(--accent);margin-top:34px}a{color:#006caa;text-decoration-thickness:1px;text-underline-offset:3px;overflow-wrap:anywhere}
p,li{overflow-wrap:anywhere}blockquote{margin:20px 0;border-right:4px solid var(--accent);background:#f0f8f6;padding:10px 22px;border-radius:7px}
code{font:13px/1.8 Consolas,'DejaVu Sans Mono',monospace;direction:ltr;unicode-bidi:isolate;background:#edf3f5;padding:2px 5px;border-radius:4px}
pre{direction:ltr;text-align:left;overflow:auto;background:#112c37;color:#e0f4f1;border-radius:10px;padding:20px;line-height:1.8}pre code{background:transparent;color:inherit;padding:0;white-space:pre}
table{border-collapse:collapse;width:100%;margin:22px 0;font-size:14px;display:block;overflow:auto}th,td{border:1px solid var(--line);padding:10px 13px;text-align:right;vertical-align:top}th{background:#eaf4f2}tr:nth-child(even){background:#f8fafb}
img{display:block;max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px;margin:22px auto}hr{border:0;border-top:1px solid var(--line);margin:34px 0}strong{font-weight:700}
footer{border-top:1px solid var(--line);padding-top:18px;margin-top:44px;color:var(--muted);font-size:13px}
@media print{body{background:white}main{border:0;margin:0;max-width:none;padding:10mm}.banner{background:white;color:black;border:1px solid #777}.banner small,.banner p{color:black}pre{white-space:pre-wrap;background:#eee;color:black}table{display:table;font-size:10px}a{color:black}h2,h3,h4{break-after:avoid}}
</style></head><body><main>
<header class="banner"><small>ARENA · MUSCLE PARADISE · HANDOFF 1.0.0 · 2026-11-24</small>
<strong>از PWA-00 شروع کن؛ کوچک بساز، مستقل بسنج.</strong>
<p>۲۸ بستهٔ پیشنهادی · ۱۷ حوزهٔ کلاینت · ابزارهای جدا از runtime · Flutter/Android محفوظ</p></header>
""" + content + """
<footer>نسخهٔ آفلاینِ HANDOFF.fa.md. تصویر در این HTML تعبیه شده؛ هیچ فونت، اسکریپت، tracker یا منبع شبکه‌ای برای خواندن لازم نیست. پیوندهای منابع هنگام کلیک به شبکه نیاز دارند. این فایل گواهی آمادگی انتشار محصول نیست.</footer>
</main></body></html>
"""
    (PAYLOAD / "HANDOFF.fa.html").write_text(document, encoding="utf-8")


def write_manifests() -> None:
    records = []
    for file in payload_files(include_manifests=False):
        data = file.read_bytes()
        records.append({"path": file.relative_to(PAYLOAD).as_posix(), "bytes": len(data), "sha256": digest(data)})
    manifest = {
        "name": NAME, "version": "1.0.0", "date_utc": "2026-11-24",
        "purpose": "Documentation handoff, not an implemented PWA or product release",
        "product_source_snapshot": "35d4b35184b4148c658b415bd009fc076bf24e00",
        "delivery_base_commit": "ded065ebaa4cb9430338889cdea3b0ed1ad57836",
        "excluded_from_this_manifest_to_avoid_self_reference": sorted(MANIFESTS),
        "files": records,
    }
    (PAYLOAD / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checksums = []
    for file in payload_files():
        if file.name == "MANIFEST.sha256":
            continue
        checksums.append(digest(file.read_bytes()) + "  " + file.relative_to(PAYLOAD).as_posix())
    (PAYLOAD / "MANIFEST.sha256").write_text("\n".join(checksums) + "\n", encoding="utf-8")


def build_zip() -> Path:
    RELEASES.mkdir(exist_ok=True)
    archive = RELEASES / (NAME + ".zip")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for file in payload_files():
            relative = file.relative_to(PAYLOAD).as_posix()
            info = zipfile.ZipInfo(NAME + "/" + relative, date_time=FIXED_ZIP_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(archive) as bundle:
        bad = bundle.testzip()
        if bad:
            raise ValueError("Corrupt ZIP member: " + bad)
    checksum = digest(archive.read_bytes())
    (RELEASES / (NAME + ".zip.sha256")).write_text(checksum + "  " + archive.name + "\n", encoding="utf-8")
    return archive


def main() -> None:
    render_html()
    write_manifests()
    archive = build_zip()
    print(f"Built {archive.relative_to(HERE.parent)} ({archive.stat().st_size:,} bytes)")
    print("SHA-256 " + digest(archive.read_bytes()))
    print("This validates packaging only, not application behavior or owner approval.")


if __name__ == "__main__":
    main()
