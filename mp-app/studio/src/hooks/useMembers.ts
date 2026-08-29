import { useEffect, useState } from 'react';

import { api, type Member } from '../api/client';

export interface UseMembers {
  members: Member[];
  loading: boolean;
  /** Non-null when the member list could not be fetched. */
  error: string | null;
}

/**
 * Load the member roster once per mount.
 *
 * Extracted because four surfaces (Operations, Programs, Coach, and the two ops
 * panels) all needed it; duplicating the fetch is how states drift apart.
 */
export function useMembers(): UseMembers {
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    void api
      .listMembers()
      .then((list) => {
        if (alive) setMembers(list);
      })
      .catch(() => {
        if (alive) setError('دریافت فهرست اعضا ناموفق بود');
      })
      .finally(() => {
        if (alive) setLoading(false);
      });
    return () => {
      alive = false;
    };
  }, []);

  return { members, loading, error };
}
