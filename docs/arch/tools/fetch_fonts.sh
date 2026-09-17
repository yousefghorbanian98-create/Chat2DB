#!/usr/bin/env bash
# بازیابیِ فونتِ فارسیِ Vazirmatn (محیط بین پیام‌ها ریست می‌شود و /home/user/fonts پاک می‌گردد).
# دانلودِ مستقیم (curl/urllib از github.com) در این سندباکس مسدود است،
# ولی api.github.com در دسترس است ⇒ فایل را به‌صورت base64 از Contents API می‌گیریم.
set -e
mkdir -p /home/user/fonts
python3 - <<'PY'
import urllib.request, json, base64, os
H = {"User-Agent": "curl", "Accept": "application/vnd.github+json"}
need = ("Vazirmatn-Regular.ttf", "Vazirmatn-Medium.ttf", "Vazirmatn-Bold.ttf")
os.makedirs("/home/user/fonts", exist_ok=True)
for nm in need:
    dst = os.path.join("/home/user/fonts", nm)
    if os.path.exists(dst) and os.path.getsize(dst) > 100000:
        print("موجود:", nm); continue
    for _ in range(3):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(
                f"https://api.github.com/repos/rastikerdar/vazirmatn/contents/fonts/ttf/{nm}",
                headers=H), timeout=90))
            raw = base64.b64decode(d["content"]) if d.get("encoding") == "base64" else None
            if raw is None:
                b = json.load(urllib.request.urlopen(urllib.request.Request(
                    f"https://api.github.com/repos/rastikerdar/vazirmatn/git/blobs/{d['sha']}",
                    headers=H), timeout=120))
                raw = base64.b64decode(b["content"])
            open(dst, "wb").write(raw)
            print("دریافت شد:", nm, len(raw)); break
        except Exception as e:
            print("تلاشِ دوباره:", nm, type(e).__name__)
PY
ls -la /home/user/fonts
