import { AnimatePresence, motion } from 'framer-motion';
import { lazy, Suspense, useState } from 'react';

import { AuthProvider, useAuth } from './auth/AuthContext';
import { CoreStatus } from './components/CoreStatus';
import { MotionCard } from './components/MotionCard';
import { MotionButton } from './components/MotionButton';
import { Skeleton } from './components/Skeleton';
import { listVariants, pageVariants } from './motion/presets';
import { Login } from './pages/Login';

// Route-based code splitting (Performance Watchdog): recharts lives in the
// assessment chunk, so the initial launcher shell stays ~92 kB gzip.
const AssessmentJp7 = lazy(() => import('./pages/AssessmentJp7'));

type Route = 'home' | 'assessment';

const TILES: ReadonlyArray<{ key: string; fa: string; en: string; phase: string; route?: Route }> = [
  { key: 'jp7', fa: 'ارزیابی JP7', en: 'JP7 Assessment', phase: 'Phase 1', route: 'assessment' },
  { key: 'members', fa: 'اعضا', en: 'Members', phase: 'Phase 1' },
  { key: 'injuries', fa: 'آسیب‌ها', en: 'Injuries', phase: 'Phase 1' },
  { key: 'attendance', fa: 'حضور و غیاب', en: 'Attendance', phase: 'Phase 2' },
  { key: 'payments', fa: 'پرداخت‌ها', en: 'Payments', phase: 'Phase 2' },
  { key: 'programs', fa: 'برنامه تمرین', en: 'Programs', phase: 'Phase 3' },
  { key: 'ai', fa: 'مربی هوش مصنوعی', en: 'AI Coach', phase: 'Phase 4' },
  { key: 'sync', fa: 'همگام‌سازی', en: 'Sync', phase: 'Phase 6' },
] as const;

function Shell() {
  const { role, logout } = useAuth();
  const [route, setRoute] = useState<Route>('home');

  if (!role) return <Login />;

  const { container, item } = listVariants('dashboard');

  return (
    <AnimatePresence mode="wait">
      <motion.main
        key={route}
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
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-lg)' }}>
            {route !== 'home' && (
              <MotionButton variant="ghost" onClick={() => setRoute('home')}>
                ← خانه
              </MotionButton>
            )}
            <div>
              <h1 style={{ fontSize: 32 }}>
                Muscle Paradise <span style={{ color: 'var(--color-primary)' }}>Studio</span>
              </h1>
              <p style={{ color: 'var(--color-muted-foreground)', margin: '4px 0 0' }}>
                {route === 'home' ? 'سیستم‌عامل باشگاه' : 'ارزیابی ترکیب بدنی — جکسون-پولاک ۷'}
              </p>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-lg)' }}>
            <CoreStatus />
            <MotionButton variant="ghost" onClick={logout}>
              خروج
            </MotionButton>
          </div>
        </header>

        {route === 'home' ? (
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
            {TILES.map((tile) => {
              const target = tile.route;
              return (
              <motion.div key={tile.key} variants={item}>
                <MotionCard
                  title={tile.fa}
                  testId={`tile-${tile.key}`}
                  mode="dashboard"
                >
                  <div onClick={target ? () => setRoute(target) : undefined} style={{ cursor: 'pointer' }}>
                    <p style={{ color: 'var(--color-muted-foreground)', margin: 0 }}>
                      <span dir="ltr" className="numeric">{tile.en}</span> · {tile.phase}
                    </p>
                  </div>
                </MotionCard>
              </motion.div>
              );
            })}
          </motion.section>
        ) : (
          <Suspense
            fallback={<Skeleton label="بارگذاری صفحهٔ ارزیابی" height={400} />}
          >
            <AssessmentJp7 />
          </Suspense>
        )}
      </motion.main>
    </AnimatePresence>
  );
}

export function App() {
  return (
    <AuthProvider>
      <Shell />
    </AuthProvider>
  );
}

export default App;
