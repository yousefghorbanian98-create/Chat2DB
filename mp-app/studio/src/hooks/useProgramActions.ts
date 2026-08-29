import { useCallback, useState } from 'react';

import {
  api,
  ApiError,
  type DryRunResult,
  type GeneratedProgram,
  type ProgramTemplate,
} from '../api/client';
import type { ButtonState } from '../components/MotionButton';

export interface ProgramActions {
  genState: ButtonState;
  applyState: ButtonState;
  generate: () => void;
  dryRun: () => void;
  apply: () => void;
}

/** Mutable state the actions drive, passed as one object to keep params ≤3. */
export interface ProgramActionCtx {
  memberId: number | null;
  template: ProgramTemplate;
  draft: GeneratedProgram | null;
  setDraft: (p: GeneratedProgram | null) => void;
  setCheck: (c: DryRunResult | null) => void;
  setNotice: (n: string | null) => void;
  reload: () => void;
}

/** Plain-text detail, or the reason that matters when apply is refused. */
function describeApplyError(err: unknown): string {
  if (!(err instanceof ApiError)) return 'اعمال ناموفق بود';
  return typeof err.detail === 'string' && err.detail.length > 0
    ? err.detail
    : 'فیلتر آسیب حالا این حرکات را مسدود می‌کند';
}

/**
 * The three planner actions: generate → dry-run → apply.
 *
 * Every refusal is surfaced verbatim so a coach sees the real reason rather
 * than a generic failure (C6 + C8 — re-validate on apply, never trust draft).
 */
export function useProgramActions(ctx: ProgramActionCtx): ProgramActions {
  const [genState, setGenState] = useState<ButtonState>('idle');
  const [applyState, setApplyState] = useState<ButtonState>('idle');

  const generate = useCallback(() => {
    if (ctx.memberId === null) return;
    setGenState('loading');
    ctx.setNotice(null);
    ctx.setCheck(null);
    void api
      .generateProgram(ctx.memberId, ctx.template)
      .then((prog) => {
        ctx.setDraft(prog);
        setGenState('success');
        ctx.reload();
      })
      .catch((err: unknown) => {
        setGenState('error');
        ctx.setNotice(err instanceof ApiError ? err.detail : 'ساخت برنامه ناموفق بود');
      });
  }, [ctx]);

  const dryRun = useCallback(() => {
    if (!ctx.draft) return;
    ctx.setCheck(null);
    void api
      .dryRunProgram(ctx.draft.id)
      .then(ctx.setCheck)
      .catch((err: unknown) => {
        ctx.setNotice(err instanceof ApiError ? err.detail : 'بررسی ناموفق بود');
      });
  }, [ctx]);

  const apply = useCallback(() => {
    if (!ctx.draft) return;
    setApplyState('loading');
    void api
      .applyProgram(ctx.draft.id)
      .then((res) => {
        setApplyState('success');
        ctx.setNotice(`برنامه تأیید و اعمال شد (${res.status})`);
        ctx.reload();
      })
      .catch((err: unknown) => {
        setApplyState('error');
        ctx.setNotice(describeApplyError(err));
      });
  }, [ctx]);

  return { genState, applyState, generate, dryRun, apply };
}
