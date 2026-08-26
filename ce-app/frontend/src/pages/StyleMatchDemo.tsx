/**
 * Example: how the new <Scoreboard /> plugs into the existing style match page.
 *
 * Replace the relevant block in `pages/StyleMatch.tsx` with this, or import the
 * component directly. The `variant` prop is the only switch you need.
 */
import { Scoreboard } from '../editor/Scoreboard'
import { analyzeApi } from '../api/analyze'

// Inside your component:
async function onBrainResult(payload: { winner: string; scoreboard: any[]; metrics?: Record<string, number> }) {
  // … existing logic that called analyzeApi.styleMatch() …
}

// In the JSX, where you used to render the scoreboard manually:
<Scoreboard
  winner={result.winner}
  scoreboard={result.scoreboard}
  metrics={result.metrics}
  elapsedSeconds={14.2}
  variant="cyberpunk"   // ← تغییر بده به "minimal" برای حالت مینیمال
  cta={
    <button
      type="button"
      className="ce-btn ce-btn--primary"
      onClick={() => applyToTimeline(result)}
    >
      {t('Apply to timeline', 'اعمال به تایم‌لاین')}
      <span className="ce-mono" style={{ marginInlineStart: 8, opacity: 0.7 }}>⏎</span>
    </button>
  }
/>
