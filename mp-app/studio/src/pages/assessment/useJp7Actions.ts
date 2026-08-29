import { useCallback, useState } from 'react';

import { api, type Assessment, type Member } from '../../api/client';
import { computeJp7, type Sex } from '../../core/jp7';
import { draftToPayload, validateDraft, type FieldError, type Jp7Draft } from '../jp7Validation';

export interface Jp7Actions {
  errors: FieldError[];
  preview: ReturnType<typeof computeJp7> | null;
  saved: Assessment | null;
  saving: boolean;
  /** Reset everything the athlete picker owns. */
  reset: () => void;
  calculate: () => void;
  save: () => void;
  validateNow: (draft: Jp7Draft) => void;
}

/**
 * JP7 calculate + save, lifted out of the page.
 *
 * The preview is client-side only; `save` asks the local core to re-derive the
 * number, so a stored value is never the client's opinion (rule JP7).
 */
export function useJp7Actions(
  draft: Jp7Draft,
  member: Member | null,
  addAssessment: (a: Assessment) => void,
): Jp7Actions {
  const [errors, setErrors] = useState<FieldError[]>([]);
  const [preview, setPreview] = useState<ReturnType<typeof computeJp7> | null>(null);
  const [saved, setSaved] = useState<Assessment | null>(null);
  const [saving, setSaving] = useState(false);

  const reset = useCallback(() => {
    setErrors([]);
    setPreview(null);
    setSaved(null);
  }, []);

  const validateNow = useCallback((d: Jp7Draft) => setErrors(validateDraft(d)), []);

  const calculate = useCallback(() => {
    const errs = validateDraft(draft);
    setErrors(errs);
    setPreview(null);
    if (errs.length > 0 || !member) return;
    const payload = draftToPayload(draft);
    setPreview(
      computeJp7({
        sex: member.sex as Sex,
        age: payload.age_years,
        sites: payload.sites_mm,
        weightKg: payload.weight_kg,
      }),
    );
  }, [draft, member]);

  const save = useCallback(() => {
    if (!member || !preview) return;
    setSaving(true);
    void api
      .saveAssessment(member.id, draftToPayload(draft))
      .then((stored) => {
        setSaved(stored);
        addAssessment(stored);
      })
      .finally(() => setSaving(false));
  }, [member, preview, draft, addAssessment]);

  return { errors, preview, saved, saving, reset, calculate, save, validateNow };
}
