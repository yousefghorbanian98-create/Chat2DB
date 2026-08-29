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
export function BodyFatChart({ history, emptyLabel = 'هنوز ارزیابی‌ای ثبت نشده است' }: BodyFatChartProps) {
  if (history.length === 0) {
    return (
      <div
        role="status"
        aria-label={emptyLabel}
        style={{
          height: 220,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'var(--color-muted-foreground)',
          border: '1px dashed var(--color-border-subtle)',
          borderRadius: 'var(--radius-md)',
        }}
      >
        {emptyLabel}
      </div>
    );
  }

  const points: Point[] = [...history]
    .sort((a, b) => a.created_at.localeCompare(b.created_at))
    .map((a) => ({
      date: toDate(a.created_at),
      bf: Number(a.body_fat_pct.toFixed(1)),
      lbm: a.lean_mass_kg,
    }));

  return (
    <div style={{ height: 220 }} dir="ltr">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={points} margin={{ top: 10, right: 12, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="bfFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#00B86A" stopOpacity={0.45} />
              <stop offset="100%" stopColor="#00B86A" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <XAxis
            dataKey="date"
            stroke="var(--color-muted-foreground)"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis
            stroke="var(--color-muted-foreground)"
            fontSize={12}
            tickLine={false}
            axisLine={false}
            domain={[0, 'dataMax + 10']}
            width={34}
          />
          <Tooltip
            contentStyle={{
              background: 'var(--color-card-solid)',
              border: '1px solid var(--color-border-subtle)',
              borderRadius: 8,
              color: 'var(--color-foreground)',
            }}
            labelStyle={{ color: 'var(--color-muted-foreground)' }}
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
