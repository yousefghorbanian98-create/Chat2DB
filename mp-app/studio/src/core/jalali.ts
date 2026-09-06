/**
 * Deterministic Gregorian → Jalali conversion (no dependency, no locale API).
 *
 * `Intl.DateTimeFormat('fa-IR-u-ca-persian')` is not available in every runtime
 * we target (older kiosks, jsdom), so the arithmetic lives here instead — the
 * algorithm is the published jalaali-js one (MIT), reproduced verbatim so the
 * leap-year breaks match the Persian calendar's observed 33-year cycle.
 */

const BREAKS = [
  -61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210, 1635, 2060, 2097, 2192, 2262, 2324, 2394,
  2456, 3178,
];

const PERSIAN_DIGITS = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

/** Truncating integer division (jalaali-js `div`). */
function div(a: number, b: number): number {
  return Math.trunc(a / b);
}

/** Remainder with the sign of the dividend (jalaali-js `mod`). */
function mod(a: number, b: number): number {
  return a - Math.trunc(a / b) * b;
}

/** Break-table lookup with an explicit guard (`noUncheckedIndexedAccess`). */
function brk(i: number): number {
  const v = BREAKS[i];
  if (v === undefined) throw new Error(`jalali: break index out of range: ${i}`);
  return v;
}

export interface JalaliDate {
  jy: number;
  jm: number;
  jd: number;
}

/** Gregorian year/month/day → Julian day number. */
function g2d(gy: number, gm: number, gd: number): number {
  let d =
    div((gy + div(gm - 8, 6) + 100100) * 1461, 4) +
    div(153 * mod(gm + 9, 12) + 2, 5) +
    gd -
    34840408;
  d = d - div(div(gy + 100100 + div(gm - 8, 6), 100) * 3, 4) + 752;
  return d;
}

/** Julian day number → Gregorian year/month/day. */
function d2g(jdn: number): { gy: number; gm: number; gd: number } {
  let j = 4 * jdn + 139361631;
  j = j + div(div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908;
  const i = div(mod(j, 1461), 4) * 5 + 308;
  const gd = div(mod(i, 153), 5) + 1;
  const gm = mod(div(i, 153), 12) + 1;
  const gy = div(j, 1461) - 100100 + div(8 - gm, 6);
  return { gy, gm, gd };
}

/** Leap-year state for a Jalali year: where Farvardin 1st falls in March. */
function jalCal(jy: number): { leap: number; march: number } {
  const gy = jy + 621;
  let leapJ = -14;
  let jp = brk(0);
  let jump = 0;

  for (let i = 1; i < BREAKS.length; i += 1) {
    const jm = brk(i);
    jump = jm - jp;
    if (jy < jm) break;
    leapJ = leapJ + div(jump, 33) * 8 + div(mod(jump, 33), 4);
    jp = jm;
  }

  let n = jy - jp;
  leapJ = leapJ + div(n, 33) * 8 + div(mod(n, 33) + 3, 4);
  if (mod(jump, 33) === 4 && jump - n === 4) leapJ += 1;

  const leapG = div(gy, 4) - div((div(gy, 100) + 1) * 3, 4) - 150;
  const march = 20 + leapJ - leapG;

  if (jump - n < 6) n = n - jump + div(jump + 4, 33) * 33;
  let leap = mod(mod(n + 1, 33) - 1, 4);
  if (leap === -1) leap = 4;

  return { leap, march };
}

/** Julian day number → Jalali year/month/day. */
function d2j(jdn: number): JalaliDate {
  const gy = d2g(jdn).gy;
  let jy = gy - 621;
  const r = jalCal(jy);
  const jdn1f = g2d(gy, 3, r.march);
  let k = jdn - jdn1f;

  if (k >= 0) {
    if (k <= 185) return { jy, jm: 1 + div(k, 31), jd: mod(k, 31) + 1 };
    k -= 186;
  } else {
    jy -= 1;
    k += 179;
    if (r.leap === 1) k += 1;
  }
  return { jy, jm: 7 + div(k, 30), jd: mod(k, 30) + 1 };
}

/** Latin digits → Persian digits. */
export function faDigits(value: string | number): string {
  return String(value).replace(/[0-9]/g, (d) => PERSIAN_DIGITS[Number(d)] ?? d);
}

/**
 * Convert an ISO-8601 timestamp to its Jalali calendar date.
 *
 * Only the UTC date part is used — a wall-clock date must not shift because the
 * viewer sits in another timezone.
 */
export function toJalali(iso: string): JalaliDate {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso);
  if (!m) throw new Error(`toJalali: not an ISO date: ${iso}`);
  return d2j(g2d(Number(m[1]), Number(m[2]), Number(m[3])));
}

/** Render an ISO timestamp as `۱۴۰۵/۰۶/۰۸` for Persian-first surfaces. */
export function faDate(iso: string): string {
  const { jy, jm, jd } = toJalali(iso);
  const pad = (n: number) => String(n).padStart(2, '0');
  return faDigits(`${jy}/${pad(jm)}/${pad(jd)}`);
}
