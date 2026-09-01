'use strict';
/**
 * Minimal JSON settings/session store persisted in Electron's userData dir.
 * Falls back to a `.jcode-desktop` folder next to the project when userData is
 * unavailable (e.g. plain Node preview).
 */
const fs = require('fs');
const path = require('path');

function dataDir(app) {
  try {
    if (app && app.getPath) return app.getPath('userData');
  } catch (_) {
    /* ignore */
  }
  return path.join(process.cwd(), '.jcode-desktop-data');
}

class Store {
  constructor(app) {
    this.file = path.join(dataDir(app), 'settings.json');
    this.data = { settings: {}, sessions: [] };
    this._load();
  }

  _load() {
    try {
      if (fs.existsSync(this.file)) {
        this.data = JSON.parse(fs.readFileSync(this.file, 'utf8'));
      }
    } catch (_) {
      this.data = { settings: {}, sessions: [] };
    }
    this.data.settings = this.data.settings || {};
    this.data.sessions = Array.isArray(this.data.sessions) ? this.data.sessions : [];
  }

  _save() {
    try {
      fs.mkdirSync(path.dirname(this.file), { recursive: true });
      fs.writeFileSync(this.file, JSON.stringify(this.data, null, 2));
    } catch (_) {
      /* best effort */
    }
  }

  get(key, fallback) {
    return this.data.settings[key] === undefined ? fallback : this.data.settings[key];
  }

  set(key, value) {
    this.data.settings[key] = value;
    this._save();
    return value;
  }

  setBulk(obj) {
    Object.assign(this.data.settings, obj);
    this._save();
    return this.data.settings;
  }

  get sessions() {
    return this.data.sessions;
  }

  saveSessions(sessions) {
    this.data.sessions = Array.isArray(sessions) ? sessions : [];
    this._save();
  }
}

module.exports = { Store, dataDir };
