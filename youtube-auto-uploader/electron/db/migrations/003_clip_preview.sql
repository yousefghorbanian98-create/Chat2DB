ALTER TABLE clips ADD COLUMN caption_path TEXT;
ALTER TABLE clips ADD COLUMN transcript TEXT;
ALTER TABLE clips ADD COLUMN render_options_json TEXT;
CREATE INDEX IF NOT EXISTS idx_clips_source_status ON clips(source_path,status);
