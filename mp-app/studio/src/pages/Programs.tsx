import { motion, useReducedMotion } from 'framer-motion';
import { useCallback, useEffect, useState } from 'react';

import {
  api,
  ApiError,
  type DryRunResult,
  type GeneratedProgram,
  type Member,
  type ProgramRow,
  type ProgramTemplate,
} from '../api/client';
import { MotionButton, type ButtonState } from '../components/MotionButton';
import { ProgramPreview } from '../components/ProgramPreview';
import { Skeleton } from '../components/Skeleton';

const TEMPLATES: ReadonlyArray<{ code: ProgramTemplate; fa: string }> = [
  { code: 'ppl', fa: 'فشار / کشش / پا' },
  { code: 'ul', fa: 'بالاتنه / پایین‌تنه' },
  { code: 'fb', fa: 'فول بادی' },
  { code: 'corrective', fa: 'حرکتی اصلاحی' },
];

/** Apply is only offered after a dry-run said it is safe (rules C6 + C8). */
export function Programs() {
  const reduced = useReducedMotion() ?? false;
  const [members, setMembers] = useState<Member[]>([]);
  const [memberId, setMemberId] = useState<number | null>(null);
  const [template, setTemplate] = useState<ProgramTemplate>('fb');
  const [history, setHistory] = useState<ProgramRow[]>([]);
  const [draft, setDraft] = useState<GeneratedProgram | null>(null);
  const [check, setCheck] = useState<DryRunResult | null>(null);
  const [genState, setGenState] = useState<ButtonState>('idle');
  const [applyState, setApplyState] = useState<ButtonState>('idle');
  const [notice, setNotice] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const list = await api.listMembers();
        if (alive) setMembers(list);
      } catch {
        /* the empty state covers this */
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  const reloadHistory = useCallback(async () => {
    if (memberId === null) return;
    try {
      setHistory(await api.listPrograms(memberId));
    } catch {
      setHistory([]);
    }
  }, [memberId]);

  useEffect(() => {
    setDraft(null);
    setCheck(null);
    setNotice(null);
    void reloadHistory();
  }, [memberId, reloadHistory]);

  async function generate() {
    if (memberId === null) return;
    setGenState('loading');
    setNotice(null);
    setCheck(null);
    try {
      setDraft(await api.generateProgram(memberId, template));
      setGenState('success');
      await reloadHistory();
    } catch (err) {
      setGenState('error');
      setNotice(err instanceof ApiError ? err.detail : 'ساخت برنامه ناموفق بود');
    }
  }

  async function dryRun() {
    if (!draft) return;
    setCheck(null);
    try {
      setCheck(await api.dryRunProgram(draft.id));
    } catch (err) {
      setNotice(err instanceof ApiError ? err.detail : 'بررسی ناموفق بود');
    }
  }

  async function apply() {
    if (!draft) return;
    setApplyState('loading');
    try {
      const res = await api.applyProgram(draft.id);
      setApplyState('success');
      setNotice(`برنامه تأیید و اعمال شد (${res.status})`);
      await reloadHistory();
    } catch (err) {
      setApplyState('error');
      setNotice(
        err instanceof ApiError
          ? typeof err.detail === 'string'
            ? err.detail
            : 'فیلتر آسیب حالا این حرکات را مسدود می‌کند'
          : 'اعمال ناموفق بود',
      );
    }
  }

  if (loading) return <Skeleton label="بارگذاری برنامه‌ها" height={320} />;

  const safeToApply = check?.safe_to_apply === true;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-lg)', alignItems: 'end' }}>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 6, minWidth: 240 }}>
          <span style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>عضو</span>
          <select
            data-testid="programs-member"
            className="mp-input"
            value={memberId ?? ''}
            onChange={(e) => setMemberId(e.target.value ? Number(e.target.value) : null)}
          >
            <option value="">— انتخاب کنید —</option>
            {members.map((m) => (
              <option key={m.id} value={m.id}>
                {m.first_name} {m.last_name} · {m.membership_code}
              </option>
            ))}
          </select>
        </label>

        <fieldset style={{ border: 'none', padding: 0, margin: 0 }}>
          <legend style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>قالب</legend>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {TEMPLATES.map((t) => (
              <button
                key={t.code}
                type="button"
                className="mp-chip"
                data-testid={`template-${t.code}`}
                aria-pressed={template === t.code}
                onClick={() => setTemplate(t.code)}
                style={{
                  background:
                    template === t.code ? 'var(--color-accent)' : 'transparent',
                  color:
                    template === t.code
                      ? 'var(--color-on-accent)'
                      : 'var(--color-foreground)',
                }}
              >
                {t.fa}
              </button>
            ))}
          </div>
        </fieldset>

        <MotionButton onClick={() => void generate()} state={genState} disabled={memberId === null}>
          ساخت برنامه
        </MotionButton>
      </div>

      {notice && (
        <motion.p
          role="status"
          data-testid="programs-notice"
          initial={reduced ? false : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          style={{ margin: 0, fontSize: 14 }}
        >
          {notice}
        </motion.p>
      )}

      {draft ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
          <ProgramPreview program={draft} />

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-md)' }}>
            <MotionButton variant="ghost" onClick={() => void dryRun()}>
              بررسی ایمنی (dry-run)
            </MotionButton>
            <MotionButton
              onClick={() => void apply()}
              state={applyState}
              disabled={!safeToApply}
            >
              تأیید و اعمال
            </MotionButton>
          </div>

          {check ? (
            <p
              data-testid="dryrun-result"
              role="status"
              style={{
                margin: 0,
                fontSize: 14,
                color: safeToApply ? 'var(--color-accent)' : 'var(--color-destructive)',
              }}
            >
              {safeToApply
                ? 'ایمن برای اعمال — هیچ حرکتی با فیلترهای فعلی تضاد ندارد.'
                : `ناایمن — تازه مسدودشده: ${check.newly_blocked.join(', ')}`}
            </p>
          ) : (
            <p style={{ margin: 0, fontSize: 13, color: 'var(--color-muted-foreground)' }}>
              اعمال فقط بعد از بررسی ایمنی فعال می‌شود.
            </p>
          )}
        </div>
      ) : (
        <p style={{ margin: 0, color: 'var(--color-muted-foreground)' }}>
          یک عضو و قالب انتخاب کنید تا برنامهٔ قانون‌محور ساخته شود.
        </p>
      )}

      <section data-testid="program-history" style={{ fontSize: 13 }}>
        <h3 style={{ fontSize: 16, marginBottom: 8 }}>تاریخچه</h3>
        {history.length === 0 ? (
          <p style={{ margin: 0, color: 'var(--color-muted-foreground)' }}>هنوز برنامه‌ای نیست.</p>
        ) : (
          <ul style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8 }}>
            {history.map((p) => (
              <li key={p.id}>
                #{p.id} · {p.title} · <strong>{p.status}</strong> ·{' '}
                <span dir="ltr">{p.source}</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default Programs;
