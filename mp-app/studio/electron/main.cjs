// MP Studio Electron main process (Phase 0 hello shell).
// Security per map §15: contextIsolation ON, nodeIntegration OFF, sandbox ON.
const { app, BrowserWindow, shell } = require('electron');
const path = require('node:path');

const DEV_URL = process.env.MP_DEV_URL || 'http://127.0.0.1:5173';

function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 900,
    backgroundColor: '#0B0F14',
    title: 'Muscle Paradise — Studio',
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  if (process.env.MP_DEV === '1') {
    win.loadURL(DEV_URL);
    win.webContents.openDevTools({ mode: 'detach' });
  } else {
    win.loadFile(path.join(__dirname, '..', 'dist', 'index.html'));
  }

  // Never let the renderer navigate the shell to an external origin.
  win.webContents.setWindowOpenHandler(({ url }) => {
    void shell.openExternal(url);
    return { action: 'deny' };
  });
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
