import { AnimatePresence, motion, type MotionStyle } from 'framer-motion';
import { useCoreHealth } from '../hooks/useCoreHealth';
import { durations, springs } from '../motion/presets';
import { Skeleton } from './Skeleton';

const PILL: MotionStyle = {
  display: 'inline-flex',
  alignItems: 'center',
  gap: 'var(--space-md)',
  padding: '6px 12px',
  borderRadius: 999,
  border: '1px solid var(--color-border-subtle)',
  fontSize: 13,
  transition: `color ${durations.normal}s`,
};

/** Pulsing dot: alive means the local core answered /health in the last 5s. */
function StatusDot({ online }: { online: boolean }) {
  const dot: MotionStyle = {
    width: 8,
    height: 8,
    borderRadius: '50%',
    background: online ? 'var(--color-success)' : 'var(--color-destructive)',
  };
  return (
    <motion.span
      aria-hidden
      animate={online ? { scale: [1, 1.25, 1] } : { scale: 1 }}
      transition={{ duration: 1.6, repeat: online ? Infinity : 0 }}
      style={dot}
    />
  );
}

/**
 * Local-core status pill: loading -> online/offline, with an animated swap.
 *
 * The Studio shell must never render a blank header while it discovers whether
 * the Python core on :8751 is up (map: Studio polls /health before rendering).
 */
export function CoreStatus() {
  const { phase, detail } = useCoreHealth();

  if (phase === 'loading') {
    return <Skeleton label="بررسی وضعیت هستهٔ محلی" height={22} width={260} />;
  }

  const online = phase === 'online';

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={phase}
        data-testid="mp-core-status"
        data-phase={phase}
        role="status"
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -6 }}
        transition={springs.snappy}
        style={PILL}
      >
        <StatusDot online={online} />
        <span className="numeric" dir="ltr">
          {online ? detail : `هستهٔ محلی در دسترس نیست — ${detail}`}
        </span>
      </motion.div>
    </AnimatePresence>
  );
}
