import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { PKGS, type PkgId, type PkgConfig } from './config'
import { applyHyperTheme, THEMES_12 } from './themes12'
import { applyPalette, THEME_PALETTES } from '../hooks/useThemeMorph'

interface PkgCtx {
  pkgId: PkgId
  config: PkgConfig
  setPkg: (id: PkgId) => void
}

const Ctx = createContext<PkgCtx | null>(null)

const STORAGE_KEY = 'ml-pkg'

function readSaved(): PkgId {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved === 'hyper' ? 'hyper' : 'cosmos'
  } catch {
    return 'cosmos'
  }
}

/**
 * Settings-driven package switcher (Data Cosmos ↔ Hyperreal).
 * Selection is persisted to localStorage and applied app-wide;
 * switching also applies the package's default theme immediately.
 */
export function PkgProvider({ children }: { children: ReactNode }) {
  const [pkgId, setPkgId] = useState<PkgId>(readSaved)

  const setPkg = (id: PkgId) => {
    setPkgId(id)
    try {
      localStorage.setItem(STORAGE_KEY, id)
    } catch {
      /* ignore */
    }
    if (id === 'hyper') applyHyperTheme(THEMES_12[0], false)
    else applyPalette(THEME_PALETTES.dark)
  }

  // keep the CSS theme in sync with the persisted package on first mount
  useEffect(() => {
    if (pkgId === 'hyper') applyHyperTheme(THEMES_12[0], false)
    else applyPalette(THEME_PALETTES.dark)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return <Ctx.Provider value={{ pkgId, config: PKGS[pkgId], setPkg }}>{children}</Ctx.Provider>
}

export function usePkg(): PkgCtx {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error('usePkg must be used within PkgProvider')
  return ctx
}
