"""RBAC با casbin — ماتریس نقش/اجازه (python-casbin).

نقش‌ها: member، coach، reception، manager
قاعده: هیچ endpoint حساسی بدون guard نقش باز نمی‌ماند (M08).
"""

from __future__ import annotations

import re
import threading
from functools import lru_cache

import casbin

from app.metrics import metrics

MODEL_TEXT = """
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && keyMatch2(r.obj, p.obj) && (r.act == p.act || p.act == "*")
"""

# ماتریس اجازه‌ها (policy) — (نقش، الگوی مسیر، متد)
# نکتهٔ keyMatch2: فقط «/*» وایلدکارت است (به‌صورت /.* تفسیر می‌شود) — پس هر مسیر
# هم به‌صورت exact و هم با «/*» ثبت می‌شود.
# DENIES (D-004): ردِ صریح که بر allow اولویت دارد — برای حفظ معنای قدیمیِ
# guardهای ترکیبی (مثلاً «manager همه‌چیز به‌جز گزارش محرمانه»).
POLICIES: list[tuple[str, str, str]] = [
    # عضو: فقط دادهٔ خودش (کنترل مالکیت در service — لایهٔ ABAC بعدی)
    ("member", "/api/v1/auth/logout", "POST"),
    ("member", "/api/v1/auth/logout-all", "POST"),
    ("member", "/api/v1/auth/refresh", "POST"),
    ("member", "/api/v1/auth/sessions", "GET"),
    ("member", "/api/v1/auth/sessions/*", "DELETE"),
    ("member", "/api/v1/members/*", "GET"),
    ("member", "/api/v1/members/me", "PUT"),
    ("member", "/api/v1/face/consent", "POST"),
    ("member", "/api/v1/face/consent/revoke", "POST"),
    # ثبت چهرهٔ خودِ عضو: پیش‌تر فقط DELETE مجاز بود، در حالی که اپ عضو دکمهٔ
    # «ثبت چهره» را نشان می‌داد و همیشه ۴۰۳ می‌گرفت (M61/D1). ثبت چهره بدون
    # رضایت صریح در service رد می‌شود (`_has_active_consent`)، پس بازکردن این
    # مسیر امنیت بیومتریک را تضعیف نمی‌کند — همان قاعده‌ای که coach/reception
    # از قبل داشتند.
    ("member", "/api/v1/face/enroll", "POST"),
    ("member", "/api/v1/face/enroll/*", "DELETE"),
    ("member", "/api/v1/face/checkin", "POST"),
    ("member", "/api/v1/face/privacy-notice", "GET"),
    ("member", "/api/v1/face/deep-status", "GET"),
    ("member", "/api/v1/face/qr-token", "GET"),
    ("member", "/api/v1/face/checkin-qr", "POST"),
    ("member", "/api/v1/face/checkins/*", "POST"),
    ("member", "/api/v1/notifications/*", "GET"),
    ("member", "/api/v1/notifications/reminders/member/*", "GET"),
    ("member", "/api/v1/notifications/*", "POST"),
    ("member", "/api/v1/programs/*", "GET"),
    ("member", "/api/v1/programs/set-feedback", "POST"),
    ("member", "/api/v1/programs/sync/set-feedback", "POST"),
    ("member", "/api/v1/assessments/*", "GET"),
    ("member", "/api/v1/assessments/limb", "POST"),
    ("member", "/api/v1/axis-assessments", "GET"),
    ("member", "/api/v1/axis-assessments/*", "GET"),
    ("member", "/api/v1/payments", "GET"),
    ("member", "/api/v1/payments/*", "GET"),
    ("member", "/api/v1/payments/wallet/pay", "POST"),
    # Q6 — آغاز پرداخت و callback درگاه: عضو باید تراکنش خودش را آغاز کند.
    # کنترل «کدام تراکنش» در service (وضعیت/authority) است.
    ("member", "/api/v1/payments", "POST"),
    # QF-07: آپلود فیش فقط برای عضوِ صاحب همان پرداخت (مالکیت در service).
    ("member", "/api/v1/payments/*/receipt", "POST"),
    ("member", "/api/v1/payments/*/start", "POST"),
    ("member", "/api/v1/payments/*/callback", "POST"),
    ("member", "/api/v1/nutrition/*", "GET"),
    # G5/M73 — عضو می‌تواند فقط گزارش غذای خودش را ثبت کند؛ مالکیت member_id
    # در service با ensure_member_scope بررسی می‌شود. نوشتن کاتالوگ یا برنامه باز نمی‌شود.
    ("member", "/api/v1/nutrition/food-logs", "POST"),
    # G3/M78 — ثبت وزن روزانهٔ خود عضو برای تخمین تطبیقی؛ مالکیت در service است.
    # مجوز دقیق است و هیچ نوشتن دیگری در nutrition را باز نمی‌کند.
    ("member", "/api/v1/nutrition/weight-logs", "POST"),
    # G9 — کتابخانهٔ حرکات با تصویر: شاگرد باید حرکت برنامهٔ خودش را ببیند.
    ("member", "/api/v1/library/*", "GET"),
    # G8 (M51-c1) — چت: عضو باید بتواند گفتگوی خودش را ببیند و پیام بدهد.
    # دامنهٔ دقیق، نه `*`: فقط زیرمسیرهای گفتگو. کنترل «کدام گفتگو»
    # در chat_service._load_conversation است (مالکیت بررسی می‌شود).
    ("member", "/api/v1/chat/conversations", "GET"),
    ("member", "/api/v1/chat/conversations", "POST"),
    ("member", "/api/v1/chat/conversations/*", "GET"),
    ("member", "/api/v1/chat/conversations/*", "POST"),
    # M43-c3 (D-004): مسیرهای مهاجرت‌داده‌شده از require_roles — عضو در فرم ورودی خودش
    # (باگ REA: نبود policy برای /ai و /population ← ۴۰۳ در مسیر ثبت‌نام واقعی)
    ("member", "/api/v1/ai/program/generate", "POST"),
    ("member", "/api/v1/ai/nutrition/generate", "POST"),
    ("member", "/api/v1/ai/suggest-weight", "POST"),
    ("member", "/api/v1/population/*", "*"),
    ("member", "/api/v1/classes", "GET"),
    ("member", "/api/v1/classes/book", "POST"),
    ("member", "/api/v1/classes/cancel", "POST"),
    # مربی: ارزیابی/برنامه/اعضا (خواندن+نوشتن برنامه)
    ("coach", "/api/v1/members", "GET"),
    ("coach", "/api/v1/members", "POST"),
    ("coach", "/api/v1/members/*", "*"),
    ("coach", "/api/v1/members/memberships", "POST"),
    ("coach", "/api/v1/assessments", "GET"),
    ("coach", "/api/v1/assessments", "POST"),
    ("coach", "/api/v1/assessments/*", "*"),
    ("coach", "/api/v1/axis-assessments", "GET"),
    ("coach", "/api/v1/axis-assessments", "POST"),
    ("coach", "/api/v1/axis-assessments/*", "*"),
    ("coach", "/api/v1/programs", "GET"),
    ("reception", "/api/v1/programs", "GET"),
    ("coach", "/api/v1/admin/attendance", "GET"),
    ("coach", "/api/v1/admin/checkins", "GET"),
    ("coach", "/api/v1/programs/*", "*"),
    ("coach", "/api/v1/library/*", "GET"),
    # M43-c3 (D-004): مسیرهای مهاجرت‌داده‌شده از require_roles
    ("coach", "/api/v1/ai/program/generate", "POST"),
    ("coach", "/api/v1/ai/nutrition/generate", "POST"),
    ("coach", "/api/v1/ai/suggest-weight", "POST"),
    ("coach", "/api/v1/population/*", "*"),
    ("coach", "/api/v1/classes", "GET"),
    ("coach", "/api/v1/classes", "POST"),
    ("coach", "/api/v1/classes/book", "POST"),
    ("coach", "/api/v1/classes/cancel", "POST"),
    ("coach", "/api/v1/reports/*", "*"),
    # M45: دادهٔ واقعی استودیو — حضور و خلاصهٔ اعضا برای مربی/مدیر/پذیرش/مالک
    ("coach", "/api/v1/admin/attendance", "GET"),
    ("coach", "/api/v1/admin/checkins", "GET"),
    ("coach", "/api/v1/admin/members-summary", "GET"),
    ("reception", "/api/v1/admin/attendance", "GET"),
    ("reception", "/api/v1/admin/checkins", "GET"),
    ("reception", "/api/v1/admin/members-summary", "GET"),
    ("coach", "/api/v1/nutrition/*", "*"),
    # G8 — مربی طرف گفتگو
    ("coach", "/api/v1/chat/conversations", "GET"),
    ("coach", "/api/v1/chat/conversations", "POST"),
    ("coach", "/api/v1/chat/conversations/*", "*"),
    ("coach", "/api/v1/nutrition/plans", "POST"),
    ("coach", "/api/v1/face/*", "*"),
    ("reception", "/api/v1/face/privacy-notice", "GET"),
    ("reception", "/api/v1/face/deep-status", "GET"),
    ("coach", "/api/v1/notifications/*", "*"),
    # پذیرش: ثبت‌نام/پرداخت/چک‌این
    ("reception", "/api/v1/classes", "GET"),
    ("reception", "/api/v1/members", "GET"),
    ("reception", "/api/v1/members", "POST"),
    ("reception", "/api/v1/members/*", "*"),
    ("reception", "/api/v1/members/memberships", "POST"),
    ("reception", "/api/v1/payments", "GET"),
    ("reception", "/api/v1/payments", "POST"),
    ("reception", "/api/v1/payments/*", "*"),
    ("reception", "/api/v1/face/checkin", "POST"),
    ("reception", "/api/v1/face/checkin-qr", "POST"),
    ("reception", "/api/v1/face/consent", "POST"),
    ("reception", "/api/v1/face/consent/revoke", "POST"),
    ("reception", "/api/v1/notifications/*", "*"),
    ("reception", "/api/v1/population/*", "*"),
    # مدیر: همه‌چیز
    ("manager", "/*", "*"),
    # ادمین سیستم: دسترسی کامل (هم‌ارز manager در casbin)
    ("admin", "/*", "*"),
    # مالک سیستم: دسترسی کامل (M39-c3 — شکاف policy پیدا شد: super_admin ثبت نشده بود)
    ("super_admin", "/*", "*"),
    # ── M59: فروشگاه، کیف‌پول، دفتر قیمت ──
    # نکتهٔ طراحی: casbin فقط «خط اول» است. تفکیک admin از super_admin در
    # نوشتن کاتالوگ/قیمت/درگاه با `ensure_owner` داخل سرویس انجام می‌شود
    # (چون casbin سطح-مسیر است و «تغییر قیمت» و «دیدن قیمت» یک مسیر دارند).
    ("member", "/api/v1/shop/*", "GET"),
    ("member", "/api/v1/shop/cart", "*"),
    ("member", "/api/v1/shop/cart/*", "*"),
    ("member", "/api/v1/shop/checkout", "POST"),
    ("member", "/api/v1/shop/orders", "GET"),
    # شارژ کیف‌پول: عضو فقط از مسیر درگاه (پرداخت واقعی) — شارژ مستقیم
    # بدون پول در M59 بسته شد؛ دستی فقط پذیرش. (باگ: شارژ ۱ میلیاردی بی‌درگاه)
    ("reception", "/api/v1/shop/*", "*"),
    ("coach", "/api/v1/shop/*", "GET"),
    ("manager", "/api/v1/shop/*", "GET"),
    ("admin", "/api/v1/shop/*", "*"),
    ("super_admin", "/api/v1/shop/*", "*"),
]

# ── M59: سلسله‌مراتب و مسیرهای ارتقای نقش ──
# نقش‌های پایین‌تر از هر `g` خط: `manager` یعنی «admin نیست» و
# `admin` یعنی «super_admin نیست» — قاعدهٔ «هیچ سطحی به سطح بالاتر نمی‌رسد».
ROLE_INHERITANCE: list[tuple[str, str]] = [
    ("super_admin", "admin"),
    ("admin", "manager"),
    ("manager", "coach"),
    ("manager", "reception"),
]

# ردِ صریح (D-004) — بر allow مقدم است؛ برای حفظ معنای قدیمیِ guardهای ترکیبی:
# - گزارش محرمانه فقط admin/coach (body-comp طبق قاعدهٔ کاربر فقط admin — manager هم رد)
# - بازبینی ارزیابی فقط manager/admin (coach نباید تأیید/رد کند)
DENIES: list[tuple[str, str, str]] = [
    ("manager", "/api/v1/reports/*", "*"),
    # QF-03: مجوز شخصی فقط با مالک سیستم؛ ادمین/مدیر حتی برای دیدن آن مجاز نیست.
    ("admin", "/api/v1/admin/permissions", "*"),
    ("admin", "/api/v1/admin/permissions/*", "*"),
    ("manager", "/api/v1/admin/permissions", "*"),
    ("manager", "/api/v1/admin/permissions/*", "*"),
    ("coach", "/api/v1/axis-assessments/:id/review", "POST"),
    # ── M59 — یافتهٔ زندهٔ ۲۰۲۶-۱۱-۱۵ ──
    # `("member", "/api/v1/payments/*", "GET")` باعث می‌شد عضو عادی
    # `GET /payments/finance/summary` و `export.csv` را با ۲۰۰ بگیرد
    # (کل درآمد باشگاه + CSV همهٔ پرداخت‌ها). با TestClient و توکن member
    # تأیید شد: 200 با `{"total_paid_rial":750000,...}`.
    ("member", "/api/v1/payments/finance/*", "*"),
    # ── M60/R3 — دادهٔ مالی خالص برای پذیرش نیست ──
    # `("reception", "/payments/*", "*")` باعث می‌شد پذیرش
    # `GET /payments/finance/summary` (کل درآمد باشگاه)، `export.csv`
    # (همهٔ پرداخت‌ها) و `POST /finance/commission` را بگیرد — تأییدشده با
    # TestClient: هر سه ۲۰۰. پذیرش برای گرفتن پول به `/payments` نیاز دارد،
    # نه به گزارش درآمد. (`manager` و بالاتر مجاز می‌مانند.)
    ("reception", "/api/v1/payments/finance/*", "*"),
    # allow کلی `/payments/*` برای پذیرش شامل refund هم می‌شد؛ بازپرداخت را فقط
    # مدیر/ادمینِ دارای `finance.write` (یا مالک) انجام دهد.
    ("reception", "/api/v1/payments/*/refund", "POST"),
    # نوشتن کاتالوگ/درگاه/قیمت هرگز از مسیر member — لایهٔ دوم بعد از ensure_owner
    ("member", "/api/v1/shop/products", "POST"),
    ("member", "/api/v1/shop/products/*", "PATCH"),
    ("member", "/api/v1/shop/gateways", "POST"),
    ("member", "/api/v1/shop/gateways/*", "PUT"),
    ("member", "/api/v1/shop/prices", "POST"),
    ("member", "/api/v1/shop/change-requests", "POST"),
    ("member", "/api/v1/shop/change-requests/*", "POST"),
    ("member", "/api/v1/shop/orders/*", "PATCH"),
]


def _build_enforcer() -> casbin.Enforcer:
    model = casbin.model.Model()
    model.load_model_from_text(MODEL_TEXT)
    enforcer = casbin.Enforcer(model)
    for role, obj, act in POLICIES:
        enforcer.add_policy(role, obj, act)
    # M59 — سلسله‌مراتب نقش: `g("super_admin","admin")` یعنی super_admin
    # همهٔ اجازه‌های admin را هم دارد، ولی نه برعکس. اگر این خطوط نبودند،
    # admin و super_admin از نظر ماشین هم‌ارز می‌ماندند (باگ اصلی).
    for child, parent in ROLE_INHERITANCE:
        enforcer.add_grouping_policy(child, parent)
    return enforcer


_ENFORCER_SLOT: dict[str, casbin.Enforcer] = {}
_ENFORCER_LOCK = threading.Lock()


def get_enforcer() -> casbin.Enforcer:
    enforcer = _ENFORCER_SLOT.get("enforcer")
    if enforcer is None:
        # WP 2.4 / F‑05: ساخت تنبل با قفل — دو نخ همزمان نباید دو enforcer بسازند.
        with _ENFORCER_LOCK:
            enforcer = _ENFORCER_SLOT.get("enforcer")
            if enforcer is None:
                enforcer = _build_enforcer()
                _ENFORCER_SLOT["enforcer"] = enforcer
    return enforcer


_NUMERIC_SEGMENT = re.compile(r"(?<=/)\d+(?=/|$)")


def _normalise_path(path: str) -> str:
    """بخش‌های عددی مسیر (شناسه) را به `:id` تبدیل می‌کند.

    هیچ سیاستی بخش عددی تحت‌اللفظی ندارد (بررسی شد)، پس تصمیم با این نرمال‌سازی تغییر نمی‌کند
    (تست هم‌ارزی `test_numeric_id_normalisation_preserves_every_decision`). این کار کاردینالیتی
    کش را از «هر شناسه» به «هر الگوی مسیر» کاهش می‌دهد.
    """
    return _NUMERIC_SEGMENT.sub(":id", path)


def _decide_raw(role: str, path: str, method: str) -> bool:
    """تصمیم بدون کش: DENIES (رد صریح) بر allow مقدم است؛ سپس casbin."""
    for deny_role, deny_obj, deny_act in DENIES:
        if (
            role == deny_role
            and (deny_act == "*" or deny_act == method)
            and casbin.util.key_match2(path, deny_obj)
        ):
            return False
    return bool(get_enforcer().enforce(role, path, method))


@lru_cache(maxsize=4096)
def _decide(role: str, path: str, method: str) -> bool:
    """تصمیم کش‌شده برای مسیر نرمال‌شده. سیاست ثابت است، پس کش امن است؛ خطا کش نمی‌شود."""
    return _decide_raw(role, path, method)


def enforce_cache_clear() -> None:
    """کش تصمیم را خالی می‌کند (پس از تغییر سیاست در تست‌ها)."""
    _decide.cache_clear()


def enforce(role: str, path: str, method: str) -> bool:
    """بررسی اجازهٔ نقش برای مسیر/متد — DENIES (رد صریح) بر allow مقدم است (D-004)."""
    try:
        allowed = _decide(role, _normalise_path(path), method)
    except Exception:
        metrics.inc("mp_rbac_errors_total")
        raise
    metrics.inc("mp_rbac_decisions_total", role=role, decision="allow" if allowed else "deny")
    return allowed
