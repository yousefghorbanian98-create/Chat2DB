'use strict';
const { app, BrowserWindow, shell } = require('electron');
const path = require('path');
const { Store } = require('./store.cjs');
const { PtyManager } = require('./pty-manager.cjs');
const { registerIpc } = require('./ipc.cjs');
const jcode = require('./jcode.cjs');

const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
} else {
  main();
}

function main() {
  let win = null;

  const store = new Store(app);
  store.userDataPath = app.getPath('userData');

  const pty = new PtyManager({
    onData: (id, data) => {
      if (win && !win.isDestroyed()) win.webContents.send('terminal:data', { id, data });
    },
    onExit: (id, code, signal) => {
      if (win && !win.isDestroyed()) win.webContents.send('terminal:exit', { id, code, signal });
    }
  });

  function getJcodeState() {
    const r = jcode.resolve(store.userDataPath, process.resourcesPath || null);
    return {
      found: !!r.path,
      path: r.path,
      pid: r.pid,
      bundled: r.bundled,
      platform: process.platform,
      arch: process.arch,
      version: null
    };
  }

  function createWindow() {
    win = new BrowserWindow({
      width: 1440,
      height: 900,
      minWidth: 1080,
      minHeight: 680,
      show: false,
      frame: false,
      backgroundColor: '#000000',
      title: 'Jcode Desktop',
      icon: path.join(__dirname, '..', '..', 'resources', 'icons', 'icon.png'),
      webPreferences: {
        preload: path.join(__dirname, '..', 'preload', 'preload.cjs'),
        contextIsolation: true,
        nodeIntegration: false,
        sandbox: false,
        spellcheck: false
      }
    });

    win.once('ready-to-show', () => win.show());
    win.on('maximize', () => win.webContents.send('window:maximized', true));
    win.on('unmaximize', () => win.webContents.send('window:maximized', false));
    win.on('closed', () => {
      pty.killAll();
      win = null;
    });

    // Open external links in the user's browser, never in-app.
    win.webContents.setWindowOpenHandler(({ url }) => {
      shell.openExternal(url);
      return { action: 'deny' };
    });

    win.loadFile(path.join(__dirname, '..', 'renderer', 'index.html'));
  }

  app.whenReady().then(() => {
    registerIpc({ store, pty, getJcodeState });

    // Trigger a lazy check of the jcode engine; the renderer will ask anyway.
    app.on('second-instance', () => {
      if (win) {
        if (win.isMinimized()) win.restore();
        win.focus();
      }
    });

    createWindow();

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  });

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
  });

  app.on('before-quit', () => pty.killAll());
}
