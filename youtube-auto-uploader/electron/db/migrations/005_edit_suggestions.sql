CREATE TABLE IF NOT EXISTS edit_suggestions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_id TEXT NOT NULL,
  source_path TEXT NOT NULL,
  type TEXT NOT NULL CHECK(type IN ('filler','silence')),
  text TEXT,
  start_time REAL NOT NULL,
  end_time REAL NOT NULL,
  confidence REAL NOT NULL,
  reason TEXT,
  status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','approved','rejected')),
  created_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_edit_suggestions_source ON edit_suggestions(source_path,status,start_time);
