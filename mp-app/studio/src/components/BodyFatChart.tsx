import type { CSSProperties } from 'react';
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

import type { Assessment } from '../api/client';

interface BodyFatChartProps {
  /** Oldest-first series — BF% over time (mockup 07, bottom band). */
  history: Assessment[];
  emptyLabel?: string;
}

interface Point {
  date: string;
  bf: number;
  lbm: number | null;
}

const DATE_FMT = new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short' });

function toDate(iso: string): string {
  const parsed = new Date(iso);
  return Number.isNaN(parsed.getTime()) ? iso : DATE_FMT.format(parsed);
}

/**
 * BF% time series. Empty state is a labelled skeleton block, never a blank
 * rectangle; the area line draws in on first view (FINN-LOOP charts block).
 */
const CHART_H = 220;
const FRAME: CSSProperties = { height: CHART_H };
const EMPTY_BOX: CSSProperties = {
  height: CHART_H,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: 'var(--color-muted-foreground)',
  border: '1px dashed var(--color-border-subtle)',
  borderRadius: 'var(--radius-md)',
};
const AXIS = {
  stroke: 'var(--color-muted-foreground)',
  fontSize: 12,
  tickLine: false,
  axisLine: false,
} as const;
const TOOLTIP_BOX: CSSProperties = {
  background: 'var(--color-card-solid)',
  border: '1px solid var(--color-border-subtle)',
  borderRadius: 8,
  color: 'var(--color-foreground)',
};
const TOOLTIP_LABEL: CSSProperties = { color: 'var(--color-muted-foreground)' };

/** Never a blank block: say what is missing (FINN-LOOP empty-state rule). */
function ChartEmpty({ label }: { label: string }) {
  return (
    <div role="status" aria-label={label} style={EMPTY_BOX}>
      {label}
    </div>
  );
}

export function BodyFatChart({
  history,
  emptyLabel = 'هنوز ارزیابی‌ای ثبت نشده است',
}: BodyFatChartProps) {
  if (history.length === 0) return <ChartEmpty label={emptyLabel} />;

  const points: Point[] = [...history]
    .sort((a, b) => a.created_at.localeCompare(b.created_at))
    .map((a) => ({
      date: toDate(a.created_at),
      bf: Number(a.body_fat_pct.toFixed(1)),
      lbm: a.lean_mass_kg,
    }));

  return (
    <div style={FRAME} dir="ltr">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={points} margin={{ top: 10, right: 12, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="bfFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#00B86A" stopOpacity={0.45} />
              <stop offset="100%" stopColor="#00B86A" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <XAxis dataKey="date" {...AXIS} />
          <YAxis {...AXIS} domain={[0, 'dataMax + 10']} width={34} />
          <Tooltip
            contentStyle={TOOLTIP_BOX}
            labelStyle={TOOLTIP_LABEL}
            formatter={(value, name) =>
              name === 'bf'
                ? [`${Number(value).toFixed(1)}%`, 'Body fat']
                : [`${Number(value)} kg`, 'LBM']
            }
          />
          <Area
            type="monotone"
            dataKey="bf"
            stroke="#12D98A"
            strokeWidth={2}
            fill="url(#bfFill)"
            isAnimationActive
            animationDuration={1200}
            animationEasing="ease-out"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
