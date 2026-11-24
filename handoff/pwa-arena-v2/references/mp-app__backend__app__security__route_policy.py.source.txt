"""سیاست مؤثرِ route که از برچسب `__rbac__` روی guardها درنمی‌آید (WP 0.2 / F-12).

# چرا این فایل وجود دارد

`scripts/export_routes.py` فقط برچسب guardها (`permission`, `grant:*`, …) و
casbin را می‌خواند. سه چیز در بدنهٔ handler/service است و از روی درخت
وابستگی دیده نمی‌شود:

1. مالک‌بودن (`super_admin`) که با `if user.role != "super_admin": raise` یا
   `ensure_owner(...)` داخل service بررسی می‌شود.
2. مالکیت سطری (`ensure_member_scope` / `ensure_record_scope` / مشارکت در گفتگو).
3. توکنی که در بدنه است (`/auth/refresh`).

این فهرست‌ها تنها ادعای «مؤثر» را نگه می‌دارند؛ خود رفتار را تغییر نمی‌دهند.
گیت ماتریس زنده (`probe_contract.py matrix` + ارزیاب سه‌ارزشی WP 0.2) هر
ناهمخوانی بین این فهرست و رفتار واقعی را می‌گیرد. هر مسیری که این‌جا نیست و
رفتار مالک/مالکیت نشان دهد، در گیت شکست می‌خورد — پس فهرست نمی‌تواند بی‌صدا کهنه شود.

# محدودیت صریح

`owner_scope` یعنی «نتیجه به داده وابسته است»؛ ارزیاب ماتریس برای این سلول‌ها
هر نتیجه‌ای را می‌پذیرد. اثباتِ مالکیت سطری به تست‌های سطح service نیاز دارد.
"""

from __future__ import annotations

# کلید = (method, path الگو همان‌طور که در OpenAPI است). مقدار = مرجع کد.
SUPER_ADMIN_ONLY: dict[tuple[str, str], str] = {
    ("GET", "/api/v1/admin/retention"): "modules/privacy/router.py:_require_owner",
    ("POST", "/api/v1/admin/retention/run"): "modules/privacy/router.py:_require_owner",
    ("GET", "/api/v1/admin/users"): "modules/admin/router.py:users_list",
    ("POST", "/api/v1/admin/users/{user_id}/role"): "modules/admin/roles.py:set_role",
    ("DELETE", "/api/v1/admin/users/{user_id}/role"): "modules/admin/roles.py:revoke_role",
    ("GET", "/api/v1/admin/permissions"): "modules/admin/permissions.py:_require_owner",
    ("GET", "/api/v1/admin/permissions/known"): "modules/admin/router.py:permissions_known",
    ("POST", "/api/v1/admin/permissions"): "modules/admin/permissions.py:_require_owner",
    (
        "DELETE",
        "/api/v1/admin/permissions/{grant_id}",
    ): "modules/admin/permissions.py:_require_owner",
    ("POST", "/api/v1/shop/products"): "modules/shop/service.py:ensure_owner «ساخت محصول»",
    (
        "PATCH",
        "/api/v1/shop/products/{product_id}",
    ): "modules/shop/service.py:ensure_owner «ویرایش محصول/قیمت»",
    ("POST", "/api/v1/shop/gateways"): "modules/shop/service.py:ensure_owner «درگاه»",
    ("PUT", "/api/v1/shop/gateways/{gateway_id}"): "modules/shop/service.py:ensure_owner «درگاه»",
    ("POST", "/api/v1/shop/prices"): "modules/shop/service.py:ensure_owner «قیمت‌گذاری خدمات»",
    (
        "POST",
        "/api/v1/shop/change-requests/{request_id}/review",
    ): "modules/shop/service.py:ensure_owner «تأیید/رد»",
}

# مالکیت سطری: member فقط داده‌ای با member_id/رکورد خودش؛ گفتگو فقط برای طرفین.
_OWNER = "app/security/ownership.py ensure_member_scope/ensure_record_scope یا طرفین گفتگو"
OWNER_SCOPE: dict[tuple[str, str], str] = {
    ("GET", "/api/v1/assessments/jp7/member/{member_id}/trend"): _OWNER,
    ("GET", "/api/v1/assessments/limb/member/{member_id}/report"): _OWNER,
    ("GET", "/api/v1/assessments/member/{member_id}"): _OWNER,
    ("GET", "/api/v1/axis-assessments/member/{member_id}"): _OWNER,
    (
        "GET",
        "/api/v1/chat/conversations/{conversation_id}/messages",
    ): "modules/notification/chat_service.py طرفین گفتگو",
    (
        "POST",
        "/api/v1/chat/conversations/{conversation_id}/messages",
    ): "modules/notification/chat_service.py طرفین گفتگو",
    (
        "POST",
        "/api/v1/chat/conversations/{conversation_id}/read",
    ): "modules/notification/chat_service.py طرفین گفتگو",
    ("POST", "/api/v1/classes/book"): _OWNER,
    ("POST", "/api/v1/classes/cancel"): _OWNER,
    ("POST", "/api/v1/face/consent"): _OWNER,
    ("POST", "/api/v1/face/consent/revoke"): _OWNER,
    ("DELETE", "/api/v1/face/enroll/{member_id}"): _OWNER,
    ("GET", "/api/v1/members/me/checkins"): "نیازمند پروفایل member (فقط نقش عضو)",
    ("GET", "/api/v1/members/memberships/{membership_id}/invoice"): _OWNER,
    ("GET", "/api/v1/members/{member_id}"): _OWNER,
    ("GET", "/api/v1/members/{member_id}/memberships"): _OWNER,
    ("GET", "/api/v1/notifications/member/{member_id}"): _OWNER,
    ("GET", "/api/v1/notifications/reminders/member/{member_id}"): _OWNER,
    ("POST", "/api/v1/notifications/{notification_id}/read"): _OWNER,
    ("POST", "/api/v1/nutrition/food-logs"): _OWNER,
    ("GET", "/api/v1/nutrition/food-logs/member/{member_id}/daily"): _OWNER,
    ("GET", "/api/v1/nutrition/member/{member_id}/adaptive"): _OWNER,
    ("GET", "/api/v1/nutrition/plans/member/{member_id}"): _OWNER,
    ("POST", "/api/v1/payments"): _OWNER,
    ("GET", "/api/v1/payments/invoice/{member_id}"): _OWNER,
    ("GET", "/api/v1/payments/ledger/{member_id}"): _OWNER,
    ("POST", "/api/v1/payments/wallet/pay"): _OWNER,
    ("GET", "/api/v1/payments/wallet/{member_id}"): _OWNER,
    ("GET", "/api/v1/payments/wallet/{member_id}/transactions"): _OWNER,
    (
        "GET",
        "/api/v1/payments/{payment_id}/receipt",
    ): "modules/payments/receipts.py ensure_record_scope",
    (
        "POST",
        "/api/v1/payments/{payment_id}/start",
    ): "modules/payments/service.py ensure_record_scope",
    ("GET", "/api/v1/programs/member/{member_id}"): _OWNER,
    ("GET", "/api/v1/programs/member/{member_id}/readiness"): _OWNER,
    ("GET", "/api/v1/programs/member/{member_id}/volume"): _OWNER,
    ("POST", "/api/v1/programs/sync/set-feedback"): _OWNER,
}

# توکن در بدنه است؛ بدون آن 401 قابل‌انتظار است. عبور anonymous شرطی است.
BODY_CREDENTIAL: dict[tuple[str, str], str] = {
    ("POST", "/api/v1/auth/refresh"): "modules/auth/router.py:refresh (refresh_token در بدنه)",
}

# هیچ مسیری فعلاً sid مقید لازم ندارد (F-12 این را به ۴۰۱ نسبت داد؛ بازتولید نشد:
# علت ۴۰۱ ابطال توکن توسط کال‌های قبلیِ ماتریس بود). فیلد برای آینده نگه داشته می‌شود.
REQUIRES_BOUND_SESSION: dict[tuple[str, str], str] = {}


def declared_scopes(method: str, path: str) -> dict[str, str]:
    """قیدهای اعلامی یک عملیات → {tag: مرجع}. برچسب‌های guard اینجا نیستند."""
    key = (method.upper(), path)
    out: dict[str, str] = {}
    if key in SUPER_ADMIN_ONLY:
        out["super_admin_only"] = SUPER_ADMIN_ONLY[key]
    if key in OWNER_SCOPE:
        out["owner_scope"] = OWNER_SCOPE[key]
    if key in BODY_CREDENTIAL:
        out["body_credential"] = BODY_CREDENTIAL[key]
    if key in REQUIRES_BOUND_SESSION:
        out["requires_bound_session"] = REQUIRES_BOUND_SESSION[key]
    return out


def all_declared_keys() -> set[tuple[str, str]]:
    return (
        set(SUPER_ADMIN_ONLY)
        | set(OWNER_SCOPE)
        | set(BODY_CREDENTIAL)
        | set(REQUIRES_BOUND_SESSION)
    )
