import { motion } from 'framer-motion';

import { CoreStatus } from './components/CoreStatus';
import { MotionCard } from './components/MotionCard';
import { MotionButton } from './components/MotionButton';
import { listVariants, pageVariants } from './motion/presets';

/** Phase 0 launcher tiles — real modules arrive in Phases 1–6. */
const TILES = [
  { key: 'members', fa: 'اعضا', en: 'Members', phase: 'Phase 1' },
  { key: 'jp7', fa: 'ارزیابی JP7', en: 'JP7 Assessment', phase: 'Phase 1' },
  { key: 'injuries', fa: 'آسیب‌ها', en: 'Injuries', phase: 'Phase 1' },
  { key: 'attendance', fa: 'حضور و غیاب', en: 'Attendance', phase: 'Phase 2' },
  { key: 'payments', fa: 'پرداخت‌ها', en: 'Payments', phase: 'Phase 2' },
  { key: 'programs', fa: 'برنامه تمرین', en: 'Programs', phase: 'Phase 3' },
  { key: 'ai', fa: 'مربی هوش مصنوعی', en: 'AI Coach', phase: 'Phase 4' },
  { key: 'sync', fa: 'همگام‌سازی', en: 'Sync', phase: 'Phase 6' },
] as const;

/**
 * Phase 0 Studio shell: proves the token system, the motion system and the
 * /health contract all work end to end. Nothing here is a dead placeholder —
 * the tile grid is the real launcher layout from mockup 01/06.
 */
export function App() {
  const { container, item } = listVariants('dashboard');

  return (
    <motion.main
      variants={pageVariants('dashboard')}
      initial="hidden"
      animate="visible"
      exit="exit"
      transition={{ duration: 0.2 }}
      style={{
        minHeight: '100%',
        padding: 'var(--space-3xl)',
        display: 'flex',
        flexDirection: 'column',
        gap: 'var(--space-2xl)',
      }}
    >
      <header
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 'var(--space-xl)',
          flexWrap: 'wrap',
        }}
      >
        <div>
          <h1 style={{ fontSize: 32 }}>
            Muscle Paradise <span style={{ color: 'var(--color-primary)' }}>Studio</span>
          </h1>
          <p style={{ color: 'var(--color-muted-foreground)', margin: '4px 0 0' }}>
            سیستم‌عامل باشگاه · فاز ۰ — اسکلت
          </p>
        </div>
        <CoreStatus />
      </header>

      <motion.section
        variants={container}
        initial="hidden"
        animate="visible"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
          gap: 'var(--space-xl)',
        }}
      >
        {TILES.map((tile) => (
          <motion.div key={tile.key} variants={item}>
            <MotionCard title={tile.fa} testId={`tile-${tile.key}`} mode="dashboard">
              <p style={{ color: 'var(--color-muted-foreground)', margin: 0 }}>
                <span dir="ltr" className="numeric">
                  {tile.en}
                </span>{' '}
                · {tile.phase}
              </p>
            </MotionCard>
          </motion.div>
        ))}
      </motion.section>

      <footer style={{ display: 'flex', gap: 'var(--space-lg)' }}>
        <MotionButton onClick={() => window.location.reload()}>بارگذاری مجدد</MotionButton>
        <MotionButton variant="ghost">تنظیمات</MotionButton>
      </footer>
    </motion.main>
  );
}

export default App;
