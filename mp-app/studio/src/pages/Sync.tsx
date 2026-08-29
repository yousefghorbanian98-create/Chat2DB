import { motion, useReducedMotion } from 'framer-motion';
import type { CSSProperties } from 'react';
import type { MotionStyle } from 'framer-motion';

import type { RestoreResult, SyncDelta } from '../api/client';
import { MotionButton } from '../components/MotionButton';
import { MotionCard } from '../components/MotionCard';
import { useBackupCreate, useRestore, useSyncOps } from '../hooks/useSyncOps';
import { fieldLabel, muted, stackLg } from '../styles/blocks';

const PAGE: CSSProperties = { display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' };
const ROW: CSSProperties = { display: 'flex', flexWrap: 'wrap', gap: 'var(--space-md)' };
const CURSOR: CSSProperties = { margin: 0, fontSize: 12, opacity: 0.7 };
/** Shared note metrics — two shapes because `motion.p` and `<p>` differ. */
const NOTE_CSS: CSSProperties = { margin: 0, fontSize: 13 };
const NOTE: MotionStyle = { margin: 0, fontSize: 13 };
const ALERT: CSSProperties = { ...NOTE_CSS, color: 'var(--color-destructive)' };
const OK: CSSProperties = { ...NOTE_CSS, color: 'var(--color-accent)' };
const LEGAL: CSSProperties = { margin: 0, fontSize: 12, color: 'var(--color-muted-foreground)' };

/** Per-table change list, or the "nothing changed" state. */
function DeltaSummary({ delta }: { delta: SyncDelta }) {
  const changed = Object.entries(delta.changes);
  if (delta.total === 0) {
    return (
      <p data-testid="sync-empty" style={{ ...OK, margin: 0 }}>
        تغییری از آخرین همگام‌سازی رخ نداده است.
      </p>
    );
  }
  return (
    <>
      <p style={{ margin: '0 0 6px' }}>
        {delta.total} ردیف در {changed.length} جدول:
      </p>
      <ul style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8 }}>
        {changed.map(([table, rows]) => (
          <li key={table}>
            <span dir="ltr" className="numeric">
              {table}
            </span>{' '}
            — {rows.length}
          </li>
        ))}
      </ul>
    </>
  );
}

/** Incremental sync card: cursor in, per-table delta out. */
function SyncCard() {
  const { cursor, delta, syncState, runSync } = useSyncOps();
  return (
    <MotionCard title="همگام‌سازی افزایشی" testId="sync-card">
      <div style={stackLg}>
        <div style={ROW}>
          <MotionButton onClick={runSync} state={syncState}>
            {cursor ? 'همگام‌سازی مجدد' : 'همگام‌سازی اولیه'}
          </MotionButton>
          {cursor ? (
            <p dir="ltr" className="numeric" style={CURSOR}>
              cursor: {cursor}
            </p>
          ) : null}
        </div>

        {delta ? (
          <div data-testid="sync-result" style={{ fontSize: 14 }}>
            <DeltaSummary delta={delta} />
          </div>
        ) : (
          <p style={{ ...muted, margin: 0, fontSize: 13 }}>
            بدون نشانگر، کل داده‌ها به‌عنوان نخستین تصویر ارسال می‌شود.
          </p>
        )}
      </div>
    </MotionCard>
  );
}

/** Encryption passphrase. Never persisted anywhere (C11). */
function PasswordField({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <label style={fieldLabel}>
      <span>گذرواژهٔ رمزنگاری (حداقل ۸ نویسه)</span>
      <input
        data-testid="backup-password"
        className="mp-input"
        type="password"
        autoComplete="new-password"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </label>
  );
}

/** The base64 blob a user pastes back in to restore. */
function BlobField({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <label style={fieldLabel}>
      <span>محتوای بکاپ برای بازیابی (base64)</span>
      <textarea
        data-testid="restore-blob"
        className="mp-input"
        dir="ltr"
        rows={3}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </label>
  );
}

/** The three outcome lines: note, error, verified restore count. */
function BackupResults({
  note,
  error,
  restored,
  reduced,
}: {
  note: string | null;
  error: string | null;
  restored: RestoreResult | null;
  reduced: boolean;
}) {
  return (
    <>
      {note ? (
        <motion.p
          role="status"
          data-testid="backup-note"
          initial={reduced ? false : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          style={NOTE}
        >
          {note}
        </motion.p>
      ) : null}

      {error ? (
        <p role="alert" data-testid="restore-error" style={ALERT}>
          {error}
        </p>
      ) : null}

      {restored ? (
        <p role="status" data-testid="restore-result" style={OK}>
          بازیابی انجام شد — {restored.rows} ردیف در {Object.keys(restored.restored).length} جدول،
          با تأیید شمارش.
        </p>
      ) : null}
    </>
  );
}

/** Encrypted backup + restore card (OWNER only, enforced server-side). */
function BackupCard() {
  const reduced = useReducedMotion() ?? false;
  const backup = useBackupCreate();
  const restore = useRestore(backup.password);
  const usable = backup.password.length >= 8;

  return (
    <MotionCard title="بکاپ رمزنگاری‌شده" testId="backup-card">
      <div style={stackLg}>
        <PasswordField value={backup.password} onChange={backup.setPassword} />

        <div style={ROW}>
          <MotionButton onClick={backup.makeBackup} state={backup.backupState} disabled={!usable}>
            تهیهٔ بکاپ
          </MotionButton>
          <MotionButton
            variant="ghost"
            onClick={restore.doRestore}
            state={restore.restoreState}
            disabled={!usable || restore.text.trim() === ''}
          >
            بازیابی
          </MotionButton>
        </div>

        <BlobField value={restore.text} onChange={restore.setText} />

        <BackupResults
          note={backup.backupNote}
          error={restore.restoreError}
          restored={restore.restored}
          reduced={reduced}
        />

        <p style={LEGAL}>
          رمزنگاری با Fernet (AES-128-CBC + HMAC) و کلید PBKDF2-SHA256 با ۲۰۰٬۰۰۰ تکرار. گذرواژه
          هیچ‌جا ذخیره نمی‌شود؛ بدون آن فایل قابل خواندن نیست.
        </p>
      </div>
    </MotionCard>
  );
}

/** Phase 6: incremental sync + encrypted backup. */
export function Sync() {
  return (
    <div style={PAGE}>
      <SyncCard />
      <BackupCard />
    </div>
  );
}

export default Sync;
