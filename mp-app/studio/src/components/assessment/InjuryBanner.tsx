import { AnimatePresence, motion } from 'framer-motion';

import type { Injury } from '../../api/client';

interface InjuryBannerProps {
  /** Already filtered to active/chronic by the caller. */
  injuries: Injury[];
}

/**
 * Hard safety banner. Injuries are a hard filter in MP (rule C5), so this is
 * never dismissible — it stays on screen while the member has an active injury.
 */
export function InjuryBanner({ injuries }: InjuryBannerProps) {
  return (
    <AnimatePresence>
      {injuries.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          role="alert"
          data-testid="injury-banner"
          style={{
            padding: '8px 14px',
            borderRadius: 8,
            background: 'rgba(239,68,68,0.15)',
            border: '1px solid var(--color-injury-active)',
            color: '#FCA5A5',
            fontSize: 13,
          }}
        >
          ⚠ {injuries.length} آسیب فعال — قبل از اعمال برنامه بررسی شود
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default InjuryBanner;
