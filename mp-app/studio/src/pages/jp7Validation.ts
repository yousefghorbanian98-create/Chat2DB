/**
 * Pure, testable validation for the JP7 assessment form.
 *
 * Mirrors the page override `pages/assessment-jp7.md`:
 *   - inputs are decimal mm, validated on blur;
 *   - Calculate is blocked if any site is empty or <= 0;
 *   - ranges match the backend (1–80 mm, age 10–100, weight > 0).
 * Keeping this out of JSX means the rules are unit-tested, not vibes-tested.
 */

export const SITE_ORDER = [
  'chest',
  'midaxillary',
  'triceps',
  'subscapular',
  'abdominal',
  'suprailiac',
  'thigh',
] as const;

export type SiteKey = (typeof SITE_ORDER)[number];

/** Persian + English labels, and a short coach tip per site (side drawer). */
export const SITE_META: Record<SiteKey, { en: string; fa: string; tip: string }> = {
  chest: { en: 'Chest', fa: 'سینه', tip: 'چین مورب، نیمهٔ راه بین نوک سینه و زیر بغل.' },
  midaxillary: { en: 'Midaxillary', fa: 'زیر بغل', tip: 'خط عمودی زیر بغل، روی خط سینه.' },
  triceps: { en: 'Triceps', fa: 'پشت بازو', tip: 'عمودی، وسط پشت بازو، آرنج صاف.' },
  subscapular: { en: 'Subscapular', fa: 'زیر کتف', tip: 'مورب، زیر زاویهٔ پایینی کتف.' },
  abdominal: { en: 'Abdomen', fa: 'شکم', tip: 'عمودی، ۲ سانتی‌متری کنار ناف.' },
  suprailiac: { en: 'Suprailiac', fa: 'لگن', tip: 'مورب، بالای تیغهٔ لگن.' },
  thigh: { en: 'Thigh', fa: 'ران', tip: 'عمودی، وسط جلوی ران، وزن روی پای دیگر.' },
} as const;

export interface Jp7Draft {
  weightKg: string;
  ageYears: string;
  sites: Record<SiteKey, string>;
}

export type FieldError = { field: string; messageFa: string; messageEn: string };

export const emptyDraft = (): Jp7Draft => ({
  weightKg: '',
  ageYears: '',
  sites: {
    chest: '',
    midaxillary: '',
    triceps: '',
    subscapular: '',
    abdominal: '',
    suprailiac: '',
    thigh: '',
  },
});

const NUM = (raw: string): number => Number(raw.trim());

const isFilled = (raw: string): boolean => raw.trim().length > 0;

export function validateSite(key: SiteKey, raw: string): FieldError | null {
  if (!isFilled(raw)) {
    return { field: key, messageFa: `${SITE_META[key].fa} خالی است`, messageEn: `${SITE_META[key].en} is empty` };
  }
  const value = NUM(raw);
  if (!Number.isFinite(value)) {
    return { field: key, messageFa: `${SITE_META[key].fa} عدد نیست`, messageEn: `${SITE_META[key].en} is not a number` };
  }
  if (value <= 0) {
    return { field: key, messageFa: `${SITE_META[key].fa} باید بزرگ‌تر از صفر باشد`, messageEn: `${SITE_META[key].en} must be > 0` };
  }
  if (value > 80) {
    return { field: key, messageFa: `${SITE_META[key].fa} خارج از محدودهٔ کالیپر (۸۰mm)`, messageEn: `${SITE_META[key].en} out of caliper range (80mm)` };
  }
  return null;
}

export function validateDraft(draft: Jp7Draft): FieldError[] {
  const errors: FieldError[] = [];

  for (const site of SITE_ORDER) {
    const err = validateSite(site, draft.sites[site]);
    if (err) errors.push(err);
  }

  if (!isFilled(draft.weightKg)) {
    errors.push({ field: 'weightKg', messageFa: 'وزن خالی است', messageEn: 'Weight is empty' });
  } else {
    const w = NUM(draft.weightKg);
    if (!Number.isFinite(w) || w <= 0) {
      errors.push({ field: 'weightKg', messageFa: 'وزن باید بزرگ‌تر از صفر باشد', messageEn: 'Weight must be > 0' });
    } else if (w > 400) {
      errors.push({ field: 'weightKg', messageFa: 'وزن نامعتبر است', messageEn: 'Weight out of range' });
    }
  }

  if (!isFilled(draft.ageYears)) {
    errors.push({ field: 'ageYears', messageFa: 'سن خالی است', messageEn: 'Age is empty' });
  } else {
    const a = NUM(draft.ageYears);
    if (!Number.isInteger(a) || a < 10 || a > 100) {
      errors.push({ field: 'ageYears', messageFa: 'سن باید عدد صحیح ۱۰ تا ۱۰۰ باشد', messageEn: 'Age must be an integer 10–100' });
    }
  }

  return errors;
}

export function canCalculate(draft: Jp7Draft): boolean {
  return validateDraft(draft).length === 0;
}

export function draftToPayload(draft: Jp7Draft) {
  return {
    weight_kg: NUM(draft.weightKg),
    age_years: NUM(draft.ageYears),
    sites_mm: {
      chest: NUM(draft.sites.chest),
      midaxillary: NUM(draft.sites.midaxillary),
      triceps: NUM(draft.sites.triceps),
      subscapular: NUM(draft.sites.subscapular),
      abdominal: NUM(draft.sites.abdominal),
      suprailiac: NUM(draft.sites.suprailiac),
      thigh: NUM(draft.sites.thigh),
    },
  };
}
