'use strict';
const { contextBridge, ipcRenderer } = require('electron');

/**
 * The single, minimal surface exposed to the renderer. Everything else lives
 * behind ipcMain handlers. Renderer code never touches Node/Electron directly.
 */
contextBridge.exposeInMainWorld('jcodeAPI', {
  /* terminal */
  terminalCreate: (opts) => ipcRenderer.invoke('terminal:create', opts),
  terminalWrite: (id, data) => ipcRenderer.send('terminal:write', { id, data }),
  terminalCommand: (id, text) => ipcRenderer.send('terminal:command', { id, text }),
  terminalResize: (id, cols, rows) => ipcRenderer.send('terminal:resize', { id, cols, rows }),
  terminalKill: (id) => ipcRenderer.send('terminal:kill', id),
  terminalList: () => ipcRenderer.invoke('terminal:list'),
  onTerminalData: (cb) => ipcRenderer.on('terminal:data', (_e, p) => cb(p.id, p.data)),
  onTerminalExit: (cb) => ipcRenderer.on('terminal:exit', (_e, p) => cb(p.id, p.code, p.signal)),

  /* jcode engine */
  jcodeState: () => ipcRenderer.invoke('jcode:state'),
  jcodeEnsure: (opts) => ipcRenderer.invoke('jcode:ensure', opts),
  onJcodeProgress: (cb) => ipcRenderer.on('jcode:progress', (_e, p) => cb(p)),

  /* window controls */
  windowMinimize: () => ipcRenderer.send('window:minimize'),
  windowMaximize: () => ipcRenderer.send('window:maximize'),
  windowClose: () => ipcRenderer.send('window:close'),
  windowIsMaximized: () => ipcRenderer.invoke('window:isMaximized'),
  onWindowMaximized: (cb) => ipcRenderer.on('window:maximized', (_e, v) => cb(v)),

  /* system */
  pickFolder: () => ipcRenderer.invoke('dialog:pickFolder'),
  openExternal: (url) => ipcRenderer.send('shell:openExternal', url),
  appInfo: () => ipcRenderer.invoke('app:info'),

  /* settings */
  storeGet: (key, fallback) => ipcRenderer.invoke('store:get', key, fallback),
  storeSet: (key, value) => ipcRenderer.invoke('store:set', key, value),
  storeBulk: (obj) => ipcRenderer.invoke('store:bulk', obj),
  storeSaveSessions: (sessions) => ipcRenderer.invoke('store:sessions', sessions),
  storeGetSessions: () => ipcRenderer.invoke('store:getSessions')
});
