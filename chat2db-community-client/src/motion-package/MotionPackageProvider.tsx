import {
  createContext,
  memo,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';
import {
  isMotionPackageId,
  MOTION_PACKAGES,
  MOTION_PACKAGE_STORAGE_KEY,
  type MotionPackageId,
} from './types';
import './motion-package.css';

interface MotionPackageContextValue {
  motionPackage: MotionPackageId;
  setMotionPackage: (id: MotionPackageId) => void;
}

const MotionPackageContext = createContext<MotionPackageContextValue | null>(null);

function readSavedPackage(): MotionPackageId {
  try {
    const saved = localStorage.getItem(MOTION_PACKAGE_STORAGE_KEY);
    return isMotionPackageId(saved) ? saved : 'cosmos';
  } catch {
    return 'cosmos';
  }
}

function applyPackageVars(id: MotionPackageId) {
  const vars = MOTION_PACKAGES[id].cssVars;
  const root = document.documentElement;
  Object.entries(vars).forEach(([key, value]) => {
    root.style.setProperty(key, value);
  });
  root.setAttribute('data-motion-package', id);
}

/**
 * Motion Package switcher (Data Cosmos ↔ Hyperreal).
 *
 * Mirrors the `master-loop-motions` demo: the chosen package is persisted in
 * localStorage, applied app-wide via CSS custom properties, and exposed
 * through this context so motion components can react to it.
 *
 * The full 3D/animated components of each package are installed in the later
 * phases of the Master Loop (dependencies + Section B–E integration); this
 * module is the settings + theming backbone they plug into.
 */
const MotionPackageProvider = memo<{ children?: ReactNode }>(({ children }) => {
  const [motionPackage, setMotionPackageState] = useState<MotionPackageId>(readSavedPackage);

  useEffect(() => {
    applyPackageVars(motionPackage);
  }, [motionPackage]);

  const setMotionPackage = useCallback((id: MotionPackageId) => {
    setMotionPackageState(id);
    try {
      localStorage.setItem(MOTION_PACKAGE_STORAGE_KEY, id);
    } catch {
      // storage unavailable — keep the in-memory choice
    }
    applyPackageVars(id);
  }, []);

  const value = useMemo(
    () => ({ motionPackage, setMotionPackage }),
    [motionPackage, setMotionPackage],
  );

  return <MotionPackageContext.Provider value={value}>{children}</MotionPackageContext.Provider>;
});

export function useMotionPackage(): MotionPackageContextValue {
  const ctx = useContext(MotionPackageContext);
  if (!ctx) {
    throw new Error('useMotionPackage must be used within MotionPackageProvider');
  }
  return ctx;
}

export default MotionPackageProvider;
