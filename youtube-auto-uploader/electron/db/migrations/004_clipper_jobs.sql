CREATE TABLE IF NOT EXISTS clipper_jobs (
  job_id TEXT PRIMARY KEY,
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'queued',
  phase TEXT NOT NULL DEFAULT 'queued',
  percent INTEGER NOT NULL DEFAULT 0,
  error TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_clipper_jobs_status ON clipper_jobs(status,created_at);
