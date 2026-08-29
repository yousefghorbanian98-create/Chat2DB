import { motion, useReducedMotion } from 'framer-motion';
import { useCallback, useState } from 'react';

import { api, ApiError, type RestoreResult, type SyncDelta } from '../api/client';
import { MotionButton, type ButtonState } from '../components/MotionButton';
import { MotionCard } from '../components/MotionCard';

/** Turn the base64 backup into a downloadable file (no server round-trip). */
function downloadBackup(blobB64: string): void {
  const bytes = Uint8Array.from(atob(blobB64), (c) => c.charCodeAt(0));
  const url = URL.createObjectURL(new Blob([bytes], { type: 'application/octet-stream' }));
  const a = document.createElement('a');
  a.href = url;
  a.download = `mp-backup-${new Date().toISOString().slice(0, 10)}.mpbk`;
  a.click();
  URL.revokeObjectURL(url);
}

/** Local-first ops: delta sync + password-encrypted backup/restore (§12.4). */
export function Sync() {
  const reduced = useReducedMotion() ?? false;
  const [cursor, setCursor] = useState<string | null>(null);
  const [delta, setDelta] = useState<SyncDelta | null>(null);
  const [syncState, setSyncState] = useState<ButtonState>('idle');
  const [password, setPassword] = useState('');
  const [backupState, setBackupState] = useState<ButtonState>('idle');
  const [backupNote, setBackupNote] = useState<string | null>(null);
  const [restoreText, setRestoreText] = useState('');
  const [restoreState, setRestoreState] = useState<ButtonState>('idle');
  const [restored, setRestored] = useState<RestoreResult | null>(null);
  const [restoreError, setRestoreError] = useState<string | null>(null);

  const runSync = useCallback(async () => {
    setSyncState('loading');
    try {
      const d = cursor ? await api.syncDelta(cursor) : await api.syncDelta();
      setDelta(d);
      setCursor(d.cursor);
      setSyncState('success');
    } catch {
      setSyncState('error');
    }
  }, [cursor]);

  async function makeBackup() {
    setBackupState('loading');
    setBackupNote(null);
    try {
      const res = await api.createBackup(password);
      downloadBackup(res.blob_b64);
      setBackupState('success');
      setBackupNote(`فایل رمزنگاری‌شده ساخته شد (${res.bytes} بایت).`);
    } catch (err) {
      setBackupState('error');
      setBackupNote(
        err instanceof ApiError
          ? err.status === 403
            ? 'فقط OWNER می‌تواند بکاپ بگیرد.'
            : err.detail
          : 'تهیهٔ بکاپ ناموفق بود',
      );
    }
  }

  async function doRestore() {
    setRestoreState('loading');
    setRestoreError(null);
    setRestored(null);
    try {
      setRestored(await api.restoreBackup(password, restoreText.trim()));
      setRestoreState('success');
    } catch (err) {
      setRestoreState('error');
      setRestoreError(
        err instanceof ApiError
          ? err.status === 403
            ? 'فقط OWNER می‌تواند بازیابی کند.'
            : err.detail
          : 'بازیابی ناموفق بود',
      );
    }
  }

  const changed = delta ? Object.entries(delta.changes) : [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-xl)' }}>
      <MotionCard title="همگام‌سازی افزایشی" testId="sync-card">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-md)' }}>
            <MotionButton onClick={() => void runSync()} state={syncState}>
              {cursor ? 'همگام‌سازی مجدد' : 'همگام‌سازی اولیه'}
            </MotionButton>
            {cursor ? (
              <p dir="ltr" className="numeric" style={{ margin: 0, fontSize: 12, opacity: 0.7 }}>
                cursor: {cursor}
              </p>
            ) : null}
          </div>

          {delta ? (
            <div data-testid="sync-result" style={{ fontSize: 14 }}>
              {delta.total === 0 ? (
                <p data-testid="sync-empty" style={{ margin: 0, color: 'var(--color-accent)' }}>
                  تغییری از آخرین همگام‌سازی رخ نداده است.
                </p>
              ) : (
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
              )}
            </div>
          ) : (
            <p style={{ margin: 0, fontSize: 13, color: 'var(--color-muted-foreground)' }}>
              بدون نشانگر، کل داده‌ها به‌عنوان نخستین تصویر ارسال می‌شود.
            </p>
          )}
        </div>
      </MotionCard>

      <MotionCard title="بکاپ رمزنگاری‌شده" testId="backup-card">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
          <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <span style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>
              گذرواژهٔ رمزنگاری (حداقل ۸ نویسه)
            </span>
            <input
              data-testid="backup-password"
              className="mp-input"
              type="password"
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--space-md)' }}>
            <MotionButton
              onClick={() => void makeBackup()}
              state={backupState}
              disabled={password.length < 8}
            >
              تهیهٔ بکاپ
            </MotionButton>
            <MotionButton
              variant="ghost"
              onClick={() => void doRestore()}
              state={restoreState}
              disabled={password.length < 8 || restoreText.trim() === ''}
            >
              بازیابی
            </MotionButton>
          </div>

          <label style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            <span style={{ fontSize: 13, color: 'var(--color-muted-foreground)' }}>
              محتوای بکاپ برای بازیابی (base64)
            </span>
            <textarea
              data-testid="restore-blob"
              className="mp-input"
              dir="ltr"
              rows={3}
              value={restoreText}
              onChange={(e) => setRestoreText(e.target.value)}
            />
          </label>

          {backupNote ? (
            <motion.p
              role="status"
              data-testid="backup-note"
              initial={reduced ? false : { opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              style={{ margin: 0, fontSize: 13 }}
            >
              {backupNote}
            </motion.p>
          ) : null}

          {restoreError ? (
            <p
              role="alert"
              data-testid="restore-error"
              style={{ margin: 0, fontSize: 13, color: 'var(--color-destructive)' }}
            >
              {restoreError}
            </p>
          ) : null}

          {restored ? (
            <p
              role="status"
              data-testid="restore-result"
              style={{ margin: 0, fontSize: 13, color: 'var(--color-accent)' }}
            >
              بازیابی انجام شد — {restored.rows} ردیف در {Object.keys(restored.restored).length}{' '}
              جدول، با تأیید شمارش.
            </p>
          ) : null}

          <p style={{ margin: 0, fontSize: 12, color: 'var(--color-muted-foreground)' }}>
            رمزنگاری با Fernet (AES-128-CBC + HMAC) و کلید PBKDF2-SHA256 با ۲۰۰٬۰۰۰ تکرار.
            گذرواژه هیچ‌جا ذخیره نمی‌شود؛ بدون آن فایل قابل خواندن نیست.
          </p>
        </div>
      </MotionCard>
    </div>
  );
}

export default Sync;
