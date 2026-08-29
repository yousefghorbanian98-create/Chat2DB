import { SITE_META, SITE_ORDER, type FieldError, type Jp7Draft } from '../../pages/jp7Validation';
import { cardSection, cardTitle, siteGrid } from '../../styles/blocks';
import { MotionButton, type ButtonState } from '../MotionButton';
import { NumberField } from '../NumberField';

interface SiteFormProps {
  draft: Jp7Draft;
  errors: FieldError[];
  canCalculate: boolean;
  /** Save is only meaningful once a preview exists (mockup 07). */
  canSave: boolean;
  saving: boolean;
  onSiteChange: (key: (typeof SITE_ORDER)[number], value: string) => void;
  onWeightChange: (value: string) => void;
  onAgeChange: (value: string) => void;
  onBlurValidate: () => void;
  onCalculate: () => void;
  onSave: () => void;
}

function messageFor(errors: FieldError[], field: string): string | null {
  return errors.find((e) => e.field === field)?.messageFa ?? null;
}

const ACTION_ROW = { display: 'flex', gap: 'var(--space-lg)', marginTop: 'var(--space-xl)' };

/** Column 2: the seven caliper sites plus weight and age (mockup 07). */
export function SiteForm(props: SiteFormProps) {
  const { draft, errors, canCalculate, canSave, saving } = props;
  const saveState: ButtonState = saving ? 'loading' : 'idle';

  return (
    <section className="glass" style={cardSection}>
      <h3 style={cardTitle}>ضخامت چین پوستی (mm)</h3>
      <div style={siteGrid}>
        {SITE_ORDER.map((key, i) => (
          <NumberField
            key={key}
            badge={i + 1}
            label={SITE_META[key].en}
            subLabel={SITE_META[key].fa}
            value={draft.sites[key]}
            onChange={(v) => props.onSiteChange(key, v)}
            onBlur={props.onBlurValidate}
            error={messageFor(errors, key)}
          />
        ))}
        <NumberField
          label="Weight"
          subLabel="وزن"
          unit="kg"
          value={draft.weightKg}
          onChange={props.onWeightChange}
          onBlur={props.onBlurValidate}
          error={messageFor(errors, 'weightKg')}
        />
        <NumberField
          label="Age"
          subLabel="سن"
          unit="y"
          value={draft.ageYears}
          onChange={props.onAgeChange}
          onBlur={props.onBlurValidate}
          error={messageFor(errors, 'ageYears')}
        />
      </div>

      <div style={ACTION_ROW}>
        <MotionButton onClick={props.onCalculate} disabled={!canCalculate}>
          محاسبه
        </MotionButton>
        <MotionButton variant="ghost" onClick={props.onSave} state={saveState} disabled={!canSave}>
          ذخیره ارزیابی
        </MotionButton>
      </div>
    </section>
  );
}

export default SiteForm;
