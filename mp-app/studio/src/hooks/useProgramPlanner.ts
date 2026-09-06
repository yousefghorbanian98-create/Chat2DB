import { useCallback, useEffect, useState } from 'react';

import {
  api,
  type DryRunResult,
  type GeneratedProgram,
  type ProgramRow,
  type ProgramTemplate,
} from '../api/client';
import type { ButtonState } from '../components/MotionButton';
import { useProgramActions } from './useProgramActions';

export interface ProgramPlanner {
  memberId: number | null;
  setMemberId: (id: number | null) => void;
  template: ProgramTemplate;
  setTemplate: (t: ProgramTemplate) => void;
  history: ProgramRow[];
  draft: GeneratedProgram | null;
  check: DryRunResult | null;
  genState: ButtonState;
  applyState: ButtonState;
  notice: string | null;
  safeToApply: boolean;
  generate: () => void;
  dryRun: () => void;
  apply: () => void;
}

interface ProgramHistory {
  history: ProgramRow[];
  clearHistory: () => void;
  reload: () => void;
}

/**
 * The athlete's program list, refreshed on demand.
 *
 * The fetch lives in the effect body itself; `reload` bumps a key, which is
 * how generate/apply ask for a refresh without setState in an effect.
 */
function useProgramHistory(memberId: number | null): ProgramHistory {
  const [history, setHistory] = useState<ProgramRow[]>([]);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    if (memberId === null) return;
    let alive = true;
    void (async () => {
      try {
        const rows = await api.listPrograms(memberId);
        if (alive) setHistory(rows);
      } catch {
        if (alive) setHistory([]);
      }
    })();
    return () => {
      alive = false;
    };
  }, [memberId, reloadKey]);

  const clearHistory = useCallback(() => setHistory([]), []);
  const reload = useCallback(() => setReloadKey((k) => k + 1), []);

  return { history, clearHistory, reload };
}

/**
 * Program planner state: generate → dry-run → apply, with history.
 *
 * Apply stays disabled until a dry-run says it is safe (C6 + C8). The actions
 * themselves live in `useProgramActions`.
 */
export function useProgramPlanner(): ProgramPlanner {
  const [memberId, setMemberIdRaw] = useState<number | null>(null);
  const [template, setTemplate] = useState<ProgramTemplate>('fb');
  const [draft, setDraft] = useState<GeneratedProgram | null>(null);
  const [check, setCheck] = useState<DryRunResult | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const { history, clearHistory, reload } = useProgramHistory(memberId);

  /** Switching athlete clears any draft that belongs to the previous one. */
  const setMemberId = useCallback(
    (id: number | null) => {
      setMemberIdRaw(id);
      setDraft(null);
      setCheck(null);
      setNotice(null);
      clearHistory();
    },
    [clearHistory],
  );

  const actions = useProgramActions({
    memberId,
    template,
    draft,
    setDraft,
    setCheck,
    setNotice,
    reload,
  });

  return {
    memberId,
    setMemberId,
    template,
    setTemplate,
    history,
    draft,
    check,
    notice,
    genState: actions.genState,
    applyState: actions.applyState,
    safeToApply: check?.safe_to_apply === true,
    generate: actions.generate,
    dryRun: actions.dryRun,
    apply: actions.apply,
  };
}
