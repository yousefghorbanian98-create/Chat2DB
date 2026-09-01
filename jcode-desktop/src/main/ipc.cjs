'use strict';
/**
 * Wires the renderer (via preload) to the backend: pty sessions, jcode engine,
 * window controls, folder picking and settings.
 */
const { ipcMain, dialog, shell, BrowserWindow } = require('electron');
const jcode = require('./jcode.cjs');

function registerIpc({ store, pty, getJcodeState, windowControl }) {
  const send = (win, channel, payload) => {
    if (win && !win.isDestroyed()) win.webContents.send(channel, payload);
  };

  /* ----- terminal ----- */
  ipcMain.handle('terminal:create', (e, o) => {
    const state = getJcodeState();
    if (!state.path) return { ok: false, error: 'jcode-not-found' };
    const id = pty.create(state.path, o || {});
    return { ok: true, id, meta: pty.getMeta(id) };
  });

  ipcMain.on('terminal:write', (e, { id, data }) => pty.write(id, data));
  ipcMain.on('terminal:command', (e, { id, text }) => pty.sendCommand(id, text));
  ipcMain.on('terminal:resize', (e, { id, cols, rows }) => pty.resize(id, cols, rows));
  ipcMain.on('terminal:kill', (e, id) => pty.kill(id));
  ipcMain.handle('terminal:list', () => pty.list());

  /* ----- jcode engine ----- */
  ipcMain.handle('jcode:state', () => getJcodeState());

  ipcMain.handle('jcode:ensure', async (e, o) => {
    try {
      const win = BrowserWindow.fromWebContents(e.sender);
      const result = await jcode.ensure({
        userDataPath: store.userDataPath,
        processResourcesPath: process.resourcesPath || null,
        force: !!(o && o.force),
        onProgress: (p) => send(win, 'jcode:progress', p)
      });
      return { ok: true, ...result };
    } catch (err) {
      return { ok: false, error: err.message };
    }
  });

  /* ----- window controls ----- */
  ipcMain.on('window:minimize', (e) => {
    const w = BrowserWindow.fromWebContents(e.sender);
    if (w) w.minimize();
  });
  ipcMain.on('window:maximize', (e) => {
    const w = BrowserWindow.fromWebContents(e.sender);
    if (!w) return;
    if (w.isMaximized()) w.unmaximize();
    else w.maximize();
  });
  ipcMain.on('window:close', (e) => {
    const w = BrowserWindow.fromWebContents(e.sender);
    if (w) w.close();
  });
  ipcMain.handle('window:isMaximized', (e) => {
    const w = BrowserWindow.fromWebContents(e.sender);
    return !!(w && w.isMaximized());
  });

  /* ----- system ----- */
  ipcMain.handle('dialog:pickFolder', async (e) => {
    const w = BrowserWindow.fromWebContents(e.sender);
    const r = await dialog.showOpenDialog(w, { properties: ['openDirectory', 'createDirectory'] });
    if (r.canceled || !r.filePaths.length) return null;
    return r.filePaths[0];
  });
  ipcMain.on('shell:openExternal', (e, url) => {
    if (typeof url === 'string' && /^https?:\/\//i.test(url)) shell.openExternal(url);
  });
  ipcMain.handle('app:info', () => ({
    platform: process.platform,
    arch: process.arch,
    version: require('../../package.json').version,
    electron: process.versions.electron,
    node: process.versions.node
  }));

  /* ----- settings ----- */
  ipcMain.handle('store:get', (e, key, fallback) => store.get(key, fallback));
  ipcMain.handle('store:set', (e, key, value) => store.set(key, value));
  ipcMain.handle('store:bulk', (e, obj) => store.setBulk(obj || {}));
  ipcMain.handle('store:sessions', (e, sessions) => store.saveSessions(sessions));
  ipcMain.handle('store:getSessions', () => store.sessions);
}

module.exports = { registerIpc };
