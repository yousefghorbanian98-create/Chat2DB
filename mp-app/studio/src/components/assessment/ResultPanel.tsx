import type { Assessment } from '../../api/client';
import type { computeJp7 } from '../../core/jp7';
import {
  bigNumber,
  cardSection,
  cardTitle,
  muted,
  noteSmall,
  stackLg,
  twoColGrid,
} from '../../styles/blocks';
import { StatCard } from '../StatCard';

const CLASSIFICATION_FA: Record<string, string> = {
  essential: 'ضروری',
  athletic: 'ورزشکاری',
  fit: 'آماده',
  average: 'متوسط',
  overfat: 'بیش‌چربی',
  obese: 'چاق',
};

interface ResultPanelProps {
  /** Client-side preview; the server re-derives the number on save. */
  preview: ReturnType<typeof computeJp7> | null;
  saved: Assessment | null;
}

/** Server-confirmed figure. Shown next to the preview, never instead of it. */
function SavedConfirmation({ saved }: { saved: Assessment }) {
  return (
    <div data-testid="bf-saved" style={{ color: 'var(--color-success)', fontSize: 14 }}>
      ✔ ذخیره شد: BF {saved.body_fat_pct.toFixed(1)}% · چگالی{' '}
      <span dir="ltr" className="numeric">
        {saved.body_density.toFixed(4)}
      </span>
    </div>
  );
}

/** Column 3: the JP7 outcome, always labelled a preview until stored. */
export function ResultPanel({ preview, saved }: ResultPanelProps) {
  return (
    <section className="glass" style={cardSection}>
      <h3 style={cardTitle}>نتایج</h3>
      {preview ? (
        <div style={stackLg}>
          <div style={bigNumber} className="numeric" dir="ltr" data-testid="bf-preview">
            {preview.bodyFatPct.toFixed(1)}%
          </div>
          <div style={twoColGrid}>
            <StatCard
              labelFa="جرم چربی"
              labelEn="FM"
              value={preview.fatMassKg?.toFixed(1) ?? '—'}
              unit="kg"
              tone="gold"
            />
            <StatCard
              labelFa="جرم بدون چربی"
              labelEn="LBM"
              value={preview.leanMassKg?.toFixed(1) ?? '—'}
              unit="kg"
              tone="primary"
            />
            <StatCard labelFa="چگالی بدن" labelEn="BD" value={preview.bodyDensity.toFixed(4)} />
            <StatCard
              labelFa="رده"
              labelEn="Class"
              value={CLASSIFICATION_FA[preview.classification] ?? preview.classification}
            />
          </div>
          <p style={noteSmall}>پیش‌نمایش — عدد نهایی پس از ذخیره توسط هستهٔ محلی تأیید می‌شود.</p>
          {saved ? <SavedConfirmation saved={saved} /> : null}
        </div>
      ) : saved ? (
        <SavedConfirmation saved={saved} />
      ) : (
        <p style={muted}>ابتدا «محاسبه» را بزنید.</p>
      )}
    </section>
  );
}

export default ResultPanel;
