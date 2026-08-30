import { AnimatePresence, motion } from 'framer-motion'
import { PKGS, type PkgId } from './config'
import { usePkg } from './PkgProvider'

const CARDS: Array<{
  id: PkgId
  title: string
  tagline: string
  swatches: string[]
  points: string[]
}> = [
  {
    id: 'cosmos',
    title: PKGS.cosmos.label,
    tagline: PKGS.cosmos.tagline,
    swatches: ['#0a2a5e', '#1e1b4b', '#312e81', '#60a5fa'],
    points: [
      'cinematic 20,000-particle loading',
      'nebula shader landing',
      'starfield run button',
      '3 themes · HSL morph',
    ],
  },
  {
    id: 'hyper',
    title: PKGS.hyper.label,
    tagline: PKGS.hyper.tagline,
    swatches: ['#3b0764', '#7c2d12', '#0f172a', '#a78bfa'],
    points: [
      'fast 2s loading + burst flash',
      'glass landing + scramble title',
      'rainbow button + confetti + glow panel',
      '12 oklch themes · coverflow · view transitions',
    ],
  },
]

/**
 * Settings panel: choose which motion package the app uses.
 * Slides in from the right (spring), applied instantly + persisted.
 */
export default function SettingsPanel({
  open,
  onClose,
  onPick,
}: {
  open: boolean
  onClose: () => void
  onPick: (id: PkgId) => void
}) {
  const { pkgId } = usePkg()

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            className="settings-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div
            className="settings-panel"
            initial={{ x: 380 }}
            animate={{ x: 0 }}
            exit={{ x: 380 }}
            transition={{ type: 'spring', stiffness: 280, damping: 30 }}
            role="dialog"
            aria-label="Settings"
          >
            <div className="settings-head">
              <h2>⚙ Settings</h2>
              <button className="ghost-btn" onClick={onClose}>
                ✕
              </button>
            </div>
            <p className="settings-sub">motion package — applies to all screens</p>

            <div className="pkg-cards">
              {CARDS.map((c) => {
                const active = pkgId === c.id
                return (
                  <button
                    key={c.id}
                    className={`pkg-card${active ? ' active' : ''}`}
                    data-id={c.id}
                    onClick={() => {
                      onPick(c.id)
                      onClose()
                    }}
                  >
                    <div className="pkg-swatches">
                      {c.swatches.map((s, i) => (
                        <i key={i} style={{ background: s }} />
                      ))}
                    </div>
                    <b>{c.title}</b>
                    <span className="pkg-tag">{c.tagline}</span>
                    <ul>
                      {c.points.map((p, i) => (
                        <li key={i}>{p}</li>
                      ))}
                    </ul>
                    <span className="pkg-check">{active ? '✓ active now' : 'tap to switch'}</span>
                  </button>
                )
              })}
            </div>

            <div className="settings-note">
              choice is saved in localStorage · applied to loading, landing, editor & style
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
