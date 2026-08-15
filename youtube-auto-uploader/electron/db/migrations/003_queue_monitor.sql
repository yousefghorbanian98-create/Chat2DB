ALTER TABLE synced_videos ADD COLUMN upload_session_uri TEXT;
ALTER TABLE synced_videos ADD COLUMN upload_offset INTEGER DEFAULT 0;
ALTER TABLE channels ADD COLUMN consecutive_failures INTEGER DEFAULT 0;
