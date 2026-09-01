'use strict';
/**
 * Manages pseudo-terminal sessions. Each session runs the real jcode binary in
 * a PTY (via node-pty) so the full TUI experience works — colours, keys, TUI
 * layout — exactly like running `jcode` in a terminal.
 */
const os = require('os');
const path = require('path');

class PtyManager {
  /**
   * @param {object} opts
   * @param {Function} opts.onData  (sessionId, data) => void
   * @param {Function} opts.onExit  (sessionId, exitCode, signal) => void
   */
  constructor(opts) {
    this.onData = opts.onData || (() => {});
    this.onExit = opts.onExit || (() => {});
    this.sessions = new Map(); // id -> pty instance
    this.meta = new Map(); // id -> { cwd, name, pid, createdAt }
    this._counter = 0;
    // Lazily require node-pty so the module can still load for pure-UI preview.
    this.pty = null;
  }

  _loadPty() {
    if (!this.pty) this.pty = require('node-pty');
    return this.pty;
  }

  /**
   * @param {object} o { cwd, cols, rows, env, args }
   */
  create(binPath, o) {
    const pty = this._loadPty();
    const id = 's' + Date.now().toString(36) + '_' + (++this._counter);
    const cols = o.cols || 110;
    const rows = o.rows || 32;
    const cwd = o.cwd || os.homedir();
    const args = Array.isArray(o.args) ? o.args : [];

    const term = pty.spawn(binPath, args, {
      name: 'xterm-256color',
      cols,
      rows,
      cwd,
      env: {
        ...process.env,
        TERM: 'xterm-256color',
        COLORTERM: 'truecolor',
        ...(o.env || {})
      }
    });

    term.onData((data) => this.onData(id, data));
    term.onExit(({ exitCode, signal }) => {
      this.sessions.delete(id);
      this.onExit(id, exitCode, signal);
    });

    this.sessions.set(id, term);
    this.meta.set(id, {
      id,
      cwd,
      name: (o.label || path.basename(cwd) || 'session').slice(0, 40),
      pid: term.pid,
      createdAt: Date.now(),
      args
    });

    return id;
  }

  write(id, data) {
    const t = this.sessions.get(id);
    if (t) t.write(data);
  }

  sendCommand(id, text) {
    this.write(id, text + '\r');
  }

  resize(id, cols, rows) {
    const t = this.sessions.get(id);
    if (t && cols > 0 && rows > 0) {
      try {
        t.resize(Math.floor(cols), Math.floor(rows));
      } catch (_) {}
    }
  }

  kill(id) {
    const t = this.sessions.get(id);
    if (t) {
      try {
        t.kill();
      } catch (_) {}
      this.sessions.delete(id);
    }
  }

  killAll() {
    for (const id of [...this.sessions.keys()]) this.kill(id);
  }

  getMeta(id) {
    return this.meta.get(id) || null;
  }

  list() {
    return [...this.meta.values()];
  }

  has(id) {
    return this.sessions.has(id);
  }
}

module.exports = { PtyManager };
