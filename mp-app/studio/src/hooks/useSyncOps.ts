import { useCallback, useState } from 'react';

import { api, ApiError, type RestoreResult, type SyncDelta } from '../api/client';
import type { ButtonState } from '../components/MotionButton';

export interface SyncOps {
  cursor: string | null;
  delta: SyncDelta | null;
  syncState: ButtonState;
  runSync: () => void;
}

export interface BackupCreateOps {
  password: string;
  setPassword: (v: string) => void;
  backupState: ButtonState;
  backupNote: string | null;
  makeBackup: () => void;
}

export interface RestoreOps {
  text: string;
  setText: (v: string) => void;
  restoreState: ButtonState;
  restoreError: string | null;
  restored: RestoreResult | null;
  doRestore: () => void;
}

/** Size-aware confirmation — the byte count is the proof it really ran. */
function backupNoteFor(bytes: number): string {
  return `بکاپ ${bytes} بایت ساخته شد. آن را در جای امن نگه دارید — بدون گذرواژه قابل خواندن نیست.`;
}

/** Map an ApiError to a Persian reason a gym owner can act on. */
function describeError(err: unknown, fallback: string, forbidden: string): string {
  if (!(err instanceof ApiError)) return fallback;
  return err.status === 403 ? forbidden : err.detail || fallback;
}

/**
 * Incremental sync: fetch a delta, store the cursor, fetch only what changed.
 * C1 — local-first means the cursor is the local machine's own watermark.
 */
export function useSyncOps(): SyncOps {
  const [cursor, setCursor] = useState<string | null>(null);
  const [delta, setDelta] = useState<SyncDelta | null>(null);
  const [syncState, setSyncState] = useState<ButtonState>('idle');

  const runSync = useCallback(() => {
    setSyncState('loading');
    void api
      .syncDelta(cursor ?? undefined)
      .then((d) => {
        setDelta(d);
        setCursor(d.cursor);
        setSyncState('success');
      })
      .catch(() => setSyncState('error'));
  }, [cursor]);

  return { cursor, delta, syncState, runSync };
}

/**
 * Encrypted backup creation.
 *
 * The password is never stored: it lives only in this closure long enough to
 * hand it to the core for the Fernet/PBKDF2 round-trip (C11).
 */
export function useBackupCreate(): BackupCreateOps {
  const [password, setPassword] = useState('');
  const [backupState, setBackupState] = useState<ButtonState>('idle');
  const [backupNote, setBackupNote] = useState<string | null>(null);

  const makeBackup = useCallback(() => {
    setBackupState('loading');
    setBackupNote(null);
    void api
      .createBackup(password)
      .then((res) => {
        setBackupNote(backupNoteFor(res.bytes));
        setBackupState('success');
      })
      .catch((err: unknown) => {
        setBackupState('error');
        setBackupNote(
          describeError(err, 'تهیهٔ بکاپ ناموفق بود', 'فقط OWNER می‌تواند بکاپ بگیرد.'),
        );
      });
  }, [password]);

  return { password, setPassword, backupState, backupNote, makeBackup };
}

/** Restore from a pasted blob, with per-table row-count verification. */
export function useRestore(password: string): RestoreOps {
  const [text, setText] = useState('');
  const [restoreState, setRestoreState] = useState<ButtonState>('idle');
  const [restoreError, setRestoreError] = useState<string | null>(null);
  const [restored, setRestored] = useState<RestoreResult | null>(null);

  const doRestore = useCallback(() => {
    setRestoreState('loading');
    setRestoreError(null);
    setRestored(null);
    void api
      .restoreBackup(password, text.trim())
      .then((res) => {
        setRestored(res);
        setRestoreState('success');
      })
      .catch((err: unknown) => {
        setRestoreState('error');
        setRestoreError(
          describeError(err, 'بازیابی ناموفق بود', 'فقط OWNER می‌تواند بازیابی کند.'),
        );
      });
  }, [password, text]);

  return { text, setText, restoreState, restoreError, restored, doRestore };
}
