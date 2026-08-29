import { AnimatePresence, motion, type MotionStyle } from 'framer-motion';
import { lazy, Suspense, useState, type CSSProperties } from 'react';

import { AuthProvider } from './auth/AuthContext';
import { useAuth } from './auth/useAuth';
import { CoreStatus } from './components/CoreStatus';
import { MotionCard } from './components/MotionCard';
import { MotionButton } from './components/MotionButton';
import { Skeleton } from './components/Skeleton';
import { listVariants, pageVariants } from './motion/presets';
import { ClientShell } from './pages/ClientShell';
import { Login } from './pages/Login';

// Route-based code splitting (Performance Watchdog): each surface is its own
// chunk, so the launcher shell stays ~95 kB gzip and recharts never loads early.
const AssessmentJp7 = lazy(() => import('./pages/AssessmentJp7'));
const Operations = lazy(() => import('./pages/Operations'));
const Programs = lazy(() => import('./pages/Programs'));
const Coach = lazy(() => import('./pages/Coach'));
const Sync = lazy(() => import('./pages/Sync'));

type Route = 'home' | 'assessment' | 'operations' | 'programs' | 'coach' | 'sync';

interface Tile {
  key: string;
  fa: string;
  en: string;
  phase: string;
  route?: Route;
}

const TILES: readonly Tile[] = [
  { key: 'jp7', fa: 'ارزیابی JP7', en: 'JP7 Assessment', phase: 'Phase 1', route: 'assessment' },
  { key: 'members', fa: 'اعضا', en: 'Members', phase: 'Phase 1' },
  { key: 'injuries', fa: 'آسیب‌ها', en: 'Injuries', phase: 'Phase 1' },
  {
    key: 'attendance',
    fa: 'حضور و غیاب',
    en: 'Attendance',
    phase: 'Phase 2',
    route: 'operations',
  },
  { key: 'payments', fa: 'پرداخت‌ها', en: 'Payments', phase: 'Phase 2', route: 'operations' },
  { key: 'programs', fa: 'برنامه تمرین', en: 'Programs', phase: 'Phase 3', route: 'programs' },
  { key: 'ai', fa: 'مربی هوش مصنوعی', en: 'AI Coach', phase: 'Phase 4', route: 'coach' },
  { key: 'sync', fa: 'همگام‌سازی', en: 'Sync', phase: 'Phase 6', route: 'sync' },
] as const;

const SUBTITLE: Record<Route, string> = {
  home: 'سیستم‌عامل باشگاه',
  assessment: 'ارزیابی ترکیب بدنی — جکسون-پولاک ۷',
  operations: 'عملیات روزانه — ورود، پرداخت، شاخص‌ها',
  programs: 'برنامه تمرین قانون‌محور — ساخت، بررسی ایمنی، اعمال',
  coach: 'تغذیهٔ قطعی و وضعیت هوش مصنوعی',
  sync: 'همگام‌سازی افزایشی و بکاپ رمزنگاری‌شده',
};

const PAGE: MotionStyle = {
  minHeight: '100%',
  padding: 'var(--space-3xl)',
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--space-2xl)',
};
const HEADER: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  gap: 'var(--space-xl)',
  flexWrap: 'wrap',
};
const ROW: CSSProperties = { display: 'flex', alignItems: 'center', gap: 'var(--space-lg)' };
const TILE_GRID: MotionStyle = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
  gap: 'var(--space-xl)',
};

/** Launcher header: back affordance, title, core status, sign-out. */
function ShellHeader({
  route,
  onHome,
  onLogout,
}: {
  route: Route;
  onHome: () => void;
  onLogout: () => void;
}) {
  return (
    <header style={HEADER}>
      <div style={ROW}>
        {route !== 'home' && (
          <MotionButton variant="ghost" onClick={onHome}>
            ← خانه
          </MotionButton>
        )}
        <div>
          <h1 style={{ fontSize: 32 }}>
            Muscle Paradise <span style={{ color: 'var(--color-primary)' }}>Studio</span>
          </h1>
          <p style={{ color: 'var(--color-muted-foreground)', margin: '4px 0 0' }}>
            {SUBTITLE[route]}
          </p>
        </div>
      </div>
      <div style={ROW}>
        <CoreStatus />
        <MotionButton variant="ghost" onClick={onLogout}>
          خروج
        </MotionButton>
      </div>
    </header>
  );
}

/** One launcher tile. Tiles without a route are announced as not-yet-built. */
function LauncherTile({ tile, onOpen }: { tile: Tile; onOpen: (r: Route) => void }) {
  const target = tile.route;
  return (
    <MotionCard title={tile.fa} testId={`tile-${tile.key}`} mode="dashboard">
      <div
        onClick={target ? () => onOpen(target) : undefined}
        style={{ cursor: target ? 'pointer' : 'default' }}
      >
        <p style={{ color: 'var(--color-muted-foreground)', margin: 0 }}>
          <span dir="ltr" className="numeric">
            {tile.en}
          </span>{' '}
          · {tile.phase}
        </p>
      </div>
    </MotionCard>
  );
}

/** The staggered launcher grid (MASTER.md: 40–60 ms stagger, y:12, no scale). */
function LauncherGrid({ onOpen }: { onOpen: (r: Route) => void }) {
  const { container, item } = listVariants('dashboard');
  return (
    <motion.section variants={container} initial="hidden" animate="visible" style={TILE_GRID}>
      {TILES.map((tile) => (
        <motion.div key={tile.key} variants={item}>
          <LauncherTile tile={tile} onOpen={onOpen} />
        </motion.div>
      ))}
    </motion.section>
  );
}

/** Lazy surface for the active route. */
function RoutedPage({ route }: { route: Route }) {
  switch (route) {
    case 'operations':
      return <Operations />;
    case 'programs':
      return <Programs />;
    case 'coach':
      return <Coach />;
    case 'sync':
      return <Sync />;
    default:
      return <AssessmentJp7 />;
  }
}

function Shell() {
  const { role, logout } = useAuth();
  const [route, setRoute] = useState<Route>('home');

  if (!role) return <Login />;
  if (role === 'MEMBER') return <ClientShell />;

  return (
    <AnimatePresence mode="wait">
      <motion.main
        key={route}
        variants={pageVariants('dashboard')}
        initial="hidden"
        animate="visible"
        exit="exit"
        transition={{ duration: 0.2 }}
        style={PAGE}
      >
        <ShellHeader route={route} onHome={() => setRoute('home')} onLogout={logout} />
        {route === 'home' ? (
          <LauncherGrid onOpen={setRoute} />
        ) : (
          <Suspense fallback={<Skeleton label={SUBTITLE[route]} height={400} />}>
            <RoutedPage route={route} />
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
