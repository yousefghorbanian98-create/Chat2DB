/**
 * M60/R3 — یک منبع حقیقت برای نقش، مشترک بین صفحات.
 *
 * قبل از این فایل، `pages/Shop.tsx` نقش را خودش از توکن می‌خواند و بقیهٔ صفحات
 * (مالی، تحلیل‌ها، تنظیمات) **هیچ** گیتی نداشتند. یعنی:
 *   - پذیرش منوی «مالی» را می‌دید (سرور بعد از M60/R3 با ۴۰۳ رد می‌کرد، ولی
 *     UI دکمه‌ای نشان می‌داد که کار نمی‌کند — همان «دکمهٔ دکوراتیو»).
 *   - دو پیاده‌سازی جدا از یک قاعده = دو جای باگ.
 *
 * قاعده: نقش از payload توکن خوانده می‌شود، چون سرور همان را امضا کرده؛ ولی
 * **این تنها لایه نیست** — هر endpoint در بک‌اند دوباره بررسی می‌کند (rbac.py).
 * پنهان‌کردن دکمه UX است، نه امنیت.
 */

import { getAccessToken } from "./session";

export type Role = "super_admin" | "admin" | "manager" | "coach" | "reception" | "member" | "guest";

export interface NavRule {
  /** حداقل نقش‌هایی که این صفحه را می‌بینند. */
  roles: readonly Role[];
  /** توضیح چرایی — تا کسی حدس نزند. */
  why: string;
}

const ALL_STAFF: readonly Role[] = [
  "super_admin",
  "admin",
  "manager",
  "coach",
  "reception",
  "member",
];

/**
 * نگاشت صفحه → نقش‌های مجاز. آینهٔ `security/rbac.py` است؛ اگر سرور تغییر کرد
 * و این‌جا نه، گیت تست `roleNav.test.ts` این را می‌گیرد.
 */
export const PAGE_RULES: Record<string, NavRule> = {
  dashboard: { roles: ALL_STAFF, why: "خلاصهٔ روز برای همه" },
  members: { roles: ["super_admin", "admin", "manager", "coach", "reception"], why: "عضو عادی فهرست اعضا را نمی‌بیند" },
  programs: { roles: ["super_admin", "admin", "manager", "coach", "member"], why: "عضو برنامهٔ خودش را می‌بیند" },
  nutrition: { roles: ["super_admin", "admin", "manager", "coach", "member"], why: "عضو برنامهٔ غذایی خودش" },
  assessment: { roles: ["super_admin", "admin", "manager", "coach", "member"], why: "ارزیابی خودِ عضو مجاز است" },
  chat: { roles: ALL_STAFF, why: "چت برای همهٔ نقش‌ها باز است" },
  checkin: { roles: ALL_STAFF, why: "حضور برای همه" },
  // ── R3: دادهٔ مالی خالص ──
  // reception پیش‌تر منو را می‌دید ولی سرور ۴۰۳ می‌داد (DENIES در rbac.py).
  // manager و بالاتر می‌مانند؛ coach و member هرگز.
  finance: {
    roles: ["super_admin", "admin", "manager"],
    why: "درآمد باشگاه و CSV همهٔ پرداخت‌ها — reception/coach/member رد می‌شوند (rbac DENIES)",
  },
  // QF-06: هزینه‌های باشگاه — دادهٔ مالی خالص؛ همان قاعدهٔ «مالی» برای reception/coach/member.
  expenses: {
    roles: ["super_admin", "admin", "manager"],
    why: "هزینه‌ها سود/زیان باشگاه را می‌سازند؛ reception/coach/member رد می‌شوند (finance.read سرور)",
  },
  analytics: {
    roles: ["super_admin", "admin", "manager", "coach"],
    why: "تحلیل عملکرد؛ پذیرش داده‌ای برای تحلیل ندارد",
  },
  // ── R3: نوشتن پیکربندی ──
  // قیمت/محصول/درگاه فقط super_admin (خواستهٔ صریح کارفرما)؛ admin فقط
  // درخواست تغییر می‌دهد. صفحه برای admin باز است تا درخواست ببیند.
  settings: {
    roles: ["super_admin", "admin"],
    why: "تنظیمات و نقش‌ها — manager/coach/reception/member نمی‌بینند",
  },
  shop: { roles: ALL_STAFF, why: "فروشگاه برای همه باز است؛ تب‌ها داخلش گیت می‌شوند" },
};

export const ROLE_LABELS: Record<Role, string> = {
  super_admin: "مالک",
  admin: "مدیر",
  manager: "سرپرست",
  coach: "مربی",
  reception: "پذیرش",
  member: "عضو",
  guest: "مهمان",
};

/** نقش را از payload توکن می‌خواند. بدون توکن → guest (نه member). */
export function roleFromToken(token: string | null | undefined = readToken()): Role {
  if (!token) return "guest";
  try {
    const part = token.split(".")[1];
    if (!part) return "guest";
    const json = JSON.parse(atob(part.replace(/-/g, "+").replace(/_/g, "/")));
    const role = typeof json?.role === "string" ? json.role : "";
    return (role in ROLE_LABELS ? role : "guest") as Role;
  } catch {
    return "guest";
  }
}

function readToken(): string | null {
  // The token role is only a UI hint; every protected API enforces RBAC server-side.
  return getAccessToken();
}

/**
 * نقش را از توکن می‌خواند، اما اگر توکن **قابل‌پارس نباشد** `null` می‌دهد.
 *
 * تفاوت مهم است: «توکن نداریم چون وارد نشده‌ایم» با «توکن داریم ولی
 * خراب/غیر-JWT است» یکی نیست. نسخهٔ اول این فایل هر دو را `guest` می‌کرد و
 * نتیجه‌اش این شد که تست‌های موجود (با توکن `tok-123`) و کاربری که توکن
 * قدیمی دارد، منوی **کاملاً خالی** می‌دیدند — بدتر از قبل.
 */
export function parseRole(token: string | null | undefined = readToken()): Role | null {
  if (!token) return null;
  try {
    const part = token.split(".")[1];
    if (!part) return null;
    const json = JSON.parse(atob(part.replace(/-/g, "+").replace(/_/g, "/")));
    const role = typeof json?.role === "string" ? json.role : "";
    return (role in ROLE_LABELS ? role : null) as Role | null;
  } catch {
    return null;
  }
}

/** آیا این نقش این صفحه را می‌بیند؟ صفحهٔ ناشناخته → نه (fail-closed). */
export function canSeePage(page: string, role: Role): boolean {
  const rule = PAGE_RULES[page];
  if (!rule) return false;
  return rule.roles.includes(role);
}

/** فهرست صفحه‌هایی که این نقش می‌بیند — برای ساخت منو. */
export function visiblePages(role: Role): string[] {
  return Object.keys(PAGE_RULES).filter((p) => canSeePage(p, role));
}
