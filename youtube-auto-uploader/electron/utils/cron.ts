/** Minimal 5-field cron matcher: minute hour day-of-month month day-of-week. Supports "*", lists "1,2", ranges "1-5", and steps "*\/15". */
function parseField(field: string, min: number, max: number): Set<number> | null {
  const values = new Set<number>();
  for (const part of field.split(',')) {
    const stepMatch = /^(.+)\/(\d+)$/.exec(part);
    const step = stepMatch ? Number(stepMatch[2]) : 1;
    const range = stepMatch?.[1] ?? part;
    let from = min;
    let to = max;
    if (range !== '*') {
      const rangeMatch = /^(\d+)(?:-(\d+))?$/.exec(range);
      if (!rangeMatch?.[1]) return null;
      from = Number(rangeMatch[1]);
      to = rangeMatch[2] === undefined ? (stepMatch ? max : from) : Number(rangeMatch[2]);
    }
    if (!Number.isFinite(step) || step < 1 || from < min || to > max || from > to) return null;
    for (let value = from; value <= to; value += step) values.add(value);
  }
  return values.size ? values : null;
}

export function isValidCron(expression: string): boolean {
  const fields = expression.trim().split(/\s+/);
  if (fields.length !== 5) return false;
  const limits: Array<[number, number]> = [[0, 59], [0, 23], [1, 31], [1, 12], [0, 7]];
  return fields.every((field, index) => {
    const limit = limits[index];
    return limit !== undefined && parseField(field, limit[0], limit[1]) !== null;
  });
}

export function cronMatches(expression: string, date = new Date()): boolean {
  const fields = expression.trim().split(/\s+/);
  if (fields.length !== 5) return false;
  const [minute, hour, dayOfMonth, month, dayOfWeek] = fields as [string, string, string, string, string];
  const minutes = parseField(minute, 0, 59);
  const hours = parseField(hour, 0, 23);
  const days = parseField(dayOfMonth, 1, 31);
  const months = parseField(month, 1, 12);
  const weekdays = parseField(dayOfWeek, 0, 7);
  if (!minutes || !hours || !days || !months || !weekdays) return false;
  const weekday = date.getDay();
  return minutes.has(date.getMinutes()) && hours.has(date.getHours()) && days.has(date.getDate())
    && months.has(date.getMonth() + 1) && (weekdays.has(weekday) || (weekday === 0 && weekdays.has(7)));
}

/** Returns true when a cron expression has matched at least one minute between the two instants. */
export function cronDue(expression: string, since: number, until = Date.now()): boolean {
  const start = Math.max(since, until - 24 * 60 * 60 * 1000);
  for (let time = Math.ceil(start / 60_000) * 60_000; time <= until; time += 60_000) {
    if (cronMatches(expression, new Date(time))) return true;
  }
  return false;
}
