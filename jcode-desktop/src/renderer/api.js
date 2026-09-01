'use strict';
/**
 * Backend adapter. The exact same renderer code runs in two environments:
 *  1. Electron (packaged app)  -> uses window.jcodeAPI (exposed by preload)
 *  2. Browser (live preview)   -> uses fetch + WebSocket to the preview server
 */
(function () {
  const isElectron = !!(window.jcodeAPI && window.jcodeAPI.terminalCreate);
  const Backend = { isElectron };

  if (isElectron) {
    const api = window.jcodeAPI;
    const dataCbs = new Set();
    const exitCbs = new Set();
    api.onTerminalData((id, data) => dataCbs.forEach((cb) => cb(id, data)));
    api.onTerminalExit((id, code, signal) => exitCbs.forEach((cb) => cb(id, code, signal)));

    Backend.createSession = (opts) => api.terminalCreate(opts);
    Backend.write = (id, data) => api.terminalWrite(id, data);
    Backend.command = (id, text) => api.terminalCommand(id, text);
    Backend.resize = (id, cols, rows) => api.terminalResize(id, cols, rows);
    Backend.kill = (id) => api.terminalKill(id);
    Backend.onData = (cb) => dataCbs.add(cb);
    Backend.onExit = (cb) => exitCbs.add(cb);
    Backend.jcodeState = () => api.jcodeState();
    Backend.jcodeEnsure = () => api.jcodeEnsure({ force: false });
    Backend.onJcodeProgress = (cb) => api.onJcodeProgress(cb);
    Backend.pickFolder = () => api.pickFolder();
    Backend.openExternal = (url) => api.openExternal(url);
    Backend.appInfo = () => api.appInfo();
    Backend.storeGet = (k, f) => api.storeGet(k, f);
    Backend.storeSet = (k, v) => api.storeSet(k, v);
    Backend.storeBulk = (o) => api.storeBulk(o);
    Backend.storeSaveSessions = (s) => api.storeSaveSessions(s);
    Backend.storeGetSessions = () => api.storeGetSessions();
    Backend.window = {
      minimize: () => api.windowMinimize(),
      maximize: () => api.windowMaximize(),
      close: () => api.windowClose(),
      isMaximized: () => api.windowIsMaximized(),
      onMaximized: (cb) => api.onWindowMaximized(cb)
    };
  } else {
    /* ---------- browser preview bridge ---------- */
    let ws = null;
    const dataCbs = new Set();
    const exitCbs = new Set();
    const openSockets = new Map();

    function connect() {
      const proto = location.protocol === 'https:' ? 'wss' : 'ws';
      ws = new WebSocket(`${proto}://${location.host}/ws`);
      ws.onmessage = (ev) => {
        let msg;
        try { msg = JSON.parse(ev.data); } catch (_) { return; }
        if (msg.type === 'data') dataCbs.forEach((cb) => cb(msg.id, msg.data));
        else if (msg.type === 'exit') exitCbs.forEach((cb) => cb(msg.id, msg.code, msg.signal));
        else if (msg.type === 'created') { const r = openSockets.get(msg.id); if (r) { openSockets.delete(msg.id); r({ ok: true, id: msg.id, meta: msg.meta }); } }
        else if (msg.type === 'error') { const r = openSockets.get(msg.id); if (r) { openSockets.delete(msg.id); r({ ok: false, error: msg.error }); } }
      };
      ws.onclose = () => { setTimeout(connect, 1500); };
    }
    connect();

    Backend.createSession = (opts) =>
      new Promise((resolve) => {
        const id = 's' + Date.now().toString(36);
        openSockets.set(id, resolve);
        if (ws && ws.readyState === 1) {
          ws.send(JSON.stringify({ type: 'create', id, cols: opts.cols, rows: opts.rows, cwd: opts.cwd || '~' }));
        } else {
          setTimeout(() => resolve({ ok: false, error: 'offline' }), 1200);
        }
        setTimeout(() => { if (openSockets.has(id)) { openSockets.delete(id); resolve({ ok: false, error: 'timeout' }); } }, 6000);
      });
    Backend.write = (id, data) => ws && ws.readyState === 1 && ws.send(JSON.stringify({ type: 'write', id, data }));
    Backend.command = (id, text) => ws && ws.readyState === 1 && ws.send(JSON.stringify({ type: 'write', id, data: text + '\r' }));
    Backend.resize = (id, cols, rows) => ws && ws.readyState === 1 && ws.send(JSON.stringify({ type: 'resize', id, cols, rows }));
    Backend.kill = (id) => ws && ws.readyState === 1 && ws.send(JSON.stringify({ type: 'kill', id }));
    Backend.onData = (cb) => dataCbs.add(cb);
    Backend.onExit = (cb) => exitCbs.add(cb);

    Backend.jcodeState = () => Promise.resolve({ found: false, path: null, platform: 'browser', preview: true });
    Backend.jcodeEnsure = () => Promise.resolve({ ok: true, downloaded: false, note: 'preview' });
    Backend.onJcodeProgress = () => {};
    Backend.pickFolder = () => Promise.resolve(null);
    Backend.openExternal = (url) => window.open(url, '_blank');
    Backend.appInfo = () => Promise.resolve({ platform: 'browser', version: 'preview', preview: true });

    // localStorage-backed settings in preview
    Backend.storeGet = (k, f) => { try { const v = localStorage.getItem('jc:' + k); return v === null ? f : JSON.parse(v); } catch (_) { return f; } };
    Backend.storeSet = (k, v) => { try { localStorage.setItem('jc:' + k, JSON.stringify(v)); } catch (_) {} return v; };
    Backend.storeBulk = (o) => { Object.entries(o).forEach(([k, v]) => Backend.storeSet(k, v)); return o; };
    Backend.storeSaveSessions = (s) => Backend.storeSet('sessions', s);
    Backend.storeGetSessions = () => Backend.storeGet('sessions', []);

    Backend.window = {
      minimize: () => {}, maximize: () => {}, close: () => {},
      isMaximized: () => Promise.resolve(false),
      onMaximized: () => {}
    };
  }

  window.Backend = Backend;
})();
