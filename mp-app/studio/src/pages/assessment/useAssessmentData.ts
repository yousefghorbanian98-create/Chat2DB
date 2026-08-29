import { useCallback, useEffect, useState } from 'react';

import { api, type Assessment, type Injury } from '../../api/client';

export interface AssessmentData {
  assessments: Assessment[];
  injuries: Injury[];
  /** Prepend a freshly stored assessment so the trend updates without a refetch. */
  addAssessment: (a: Assessment) => void;
}

/**
 * Assessment history + injuries for one member.
 *
 * History is non-fatal: if it fails the form still works, so the failure is
 * contained here rather than poisoning the page's load phase.
 */
export function useAssessmentData(memberId: number | null): AssessmentData {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [injuries, setInjuries] = useState<Injury[]>([]);

  // Clear stale rows during render when the member changes — setState inside
  // the effect would cascade a second render (react-hooks/set-state-in-effect).
  const [prevId, setPrevId] = useState<number | null>(null);
  if (memberId !== prevId) {
    setPrevId(memberId);
    setAssessments([]);
    setInjuries([]);
  }

  useEffect(() => {
    if (memberId === null) return;
    let alive = true;
    void (async () => {
      try {
        const [assess, inj] = await Promise.all([
          api.listAssessments(memberId),
          api.listInjuries(memberId),
        ]);
        if (!alive) return;
        setAssessments(assess);
        setInjuries(inj);
      } catch {
        /* history is non-fatal for the form */
      }
    })();
    return () => {
      alive = false;
    };
  }, [memberId]);

  const addAssessment = useCallback((a: Assessment) => {
    setAssessments((prev) => [a, ...prev]);
  }, []);

  return { assessments, injuries, addAssessment };
}
