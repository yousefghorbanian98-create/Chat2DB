'use strict';
/* ============================================================
 * Jcode Desktop — renderer app logic
 * ============================================================ */
(function () {
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => Array.from(document.querySelectorAll(s));

  const Backend = window.Backend;
  const Cosmos = window.Cosmos;
  const TM = window.TerminalManager;

  const THEMES = [
    { id: 'nebula-violet', label: 'Nebula Violet', a: '#8b5cf6', b: '#06b6d4' },
    { id: 'deep-space', label: 'Deep Space', a: '#3b82f6', b: '#06b6d4' },
    { id: 'solar-flare', label: 'Solar Flare', a: '#f97316', b: '#ec4899' },
    { id: 'aurora', label: 'Aurora', a: '#10b981', b: '#22d3ee' }
  ];

  const PROVIDERS = [
    { id: 'claude', name: 'Claude', sub: 'Anthropic', icon: '✳' },
    { id: 'openai', name: 'OpenAI / ChatGPT', sub: 'ChatGPT · Codex', icon: '◉' },
    { id: 'gemini', name: 'Google Gemini', sub: 'Gemini', icon: '✦' },
    { id: 'copilot', name: 'GitHub Copilot', sub: 'Copilot plan', icon: '⌥' },
    { id: 'azure', name: 'Azure OpenAI', sub: 'Azure', icon: '☁' },
    { id: 'openrouter', name: 'OpenRouter', sub: 'many models', icon: '⌘' },
    { id: 'deepseek', name: 'DeepSeek', sub: 'deepseek', icon: '◈' },
    { id: 'kimi', name: 'Kimi', sub: 'Moonshot', icon: '✧' },
    { id: 'ollama', name: 'Ollama', sub: 'local', icon: '♆' },
    { id: 'lmstudio', name: 'LM Studio', sub: 'local', icon: '▣' },
    { id: 'fireworks', name: 'Fireworks', sub: 'fireworks.ai', icon: '✴' },
    { id: 'openai-compatible', name: 'Custom endpoint', sub: 'OpenAI-compatible', icon: '⚙' }
  ];

  const state = {
    sessions: [], // [{id,name,cwd,kind,createdAt}]
    activeId: null,
    settings: {
      theme: 'nebula-violet',
      customCursor: true,
      showPanel: true,
      fontSize: 14,
      blackhole: true,
      pulsar: true,
      nebula: true,
      starDensity: 3000,
      cosmosIntensity: 0.85,
      defaultCwd: null
    },
    engine: { found: false, path: null, platform: '…', version: null, busy: false }
  };

  /* ==================== PRELOADER ==================== */
  function runPreloader(done) {
    const bar = $('#preloader-bar');
    const pct = $('#preloader-percent');
    let p = 0;
    const iv = setInterval(() => {
      p += Math.random() * 14 + 4;
      if (p >= 100) {
        p = 100;
        clearInterval(iv);
        setTimeout(() => {
          $('#preloader').classList.add('hidden');
          done && done();
        }, 320);
      }
      bar.style.width = p + '%';
      pct.textContent = Math.floor(p) + '%';
    }, 120);
  }

  /* ==================== TOAST ==================== */
  let toastTimer = 0;
  function toast(msg, ms) {
    const t = $('#toast');
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { t.hidden = true; }, ms || 3200);
  }

  /* ==================== SETTINGS ==================== */
  async function loadSettings() {
    const s = state.settings;
    for (const k of Object.keys(s)) {
      const v = await Backend.storeGet(k, s[k]);
      if (v !== undefined && v !== null) s[k] = v;
    }
    applySettings();
  }
  function saveSettings() {
    Backend.storeBulk(state.settings);
  }
  function applySettings() {
    const s = state.settings;
    document.documentElement.dataset.theme = s.theme;
    document.body.classList.toggle('custom-cursor', !!s.customCursor);
    $('#info-panel').classList.toggle('collapsed', !s.showPanel);
    $('#opt-panel').checked = s.showPanel;
    $('#opt-cursor').checked = s.customCursor;
    $('#opt-fontsize').value = s.fontSize;
    $('#star-density').value = s.starDensity;
    $('#cosmos-intensity').value = Math.round(s.cosmosIntensity * 100);
    TM.setFontSize(s.fontSize);
    Cosmos.setOption('blackhole', s.blackhole);
    Cosmos.setOption('pulsar', s.pulsar);
    Cosmos.setOption('nebula', s.nebula);
    Cosmos.setOption('starDensity', s.starDensity);
    Cosmos.setOption('intensity', s.cosmosIntensity);
    $('#theme-swatches').innerHTML = THEMES.map((t) =>
      `<button class="swatch${s.theme === t.id ? ' active' : ''}" data-theme-id="${t.id}" style="background:linear-gradient(135deg,${t.a},${t.b})" title="${t.label}"></button>`
    ).join('');
    syncCosmosToggles();
  }
  function syncCosmosToggles() {
    const map = { 'toggle-blackhole': 'blackhole', 'toggle-pulsar': 'pulsar', 'toggle-nebula': 'nebula' };
    $$('.ip-toggle').forEach((b) => {
      const k = map[b.dataset.cmd];
      if (k !== undefined) b.classList.toggle('on', !!state.settings[k]);
    });
  }

  /* ==================== ENGINE ==================== */
  function renderEngine() {
    const e = state.engine;
    const dot = $('#engine-dot');
    const label = $('#engine-label');
    const sub = $('#engine-sub');
    const bar = $('#engine-bar-fill');
    dot.className = 'engine-dot' + (e.busy ? ' busy' : e.found ? ' ok' : ' err');
    if (e.busy) { label.textContent = 'Engine · downloading'; }
    else if (e.found) { label.textContent = 'Engine ready'; }
    else { label.textContent = 'Engine missing'; }
    if (e.busy && e.progress) sub.textContent = e.progress.phase === 'download' ? `Downloading ${e.progress.asset || ''} ${e.progress.pct || 0}%` : 'Preparing…';
    else if (e.version) sub.textContent = 'jcode ' + e.version;
    else if (e.found) sub.textContent = e.path ? e.path.split(/[\\/]/).pop() : 'jcode';
    else sub.textContent = Backend.isElectron ? 'Not installed — click to download' : 'Runs inside the desktop app';
    bar.style.width = (e.busy && e.progress && e.progress.pct) ? e.progress.pct + '%' : (e.found ? '100%' : '0%');
    $('#engine-path-desc').textContent = e.path || 'No engine binary found yet.';
  }

  async function refreshEngineState() {
    try {
      const st = await Backend.jcodeState();
      Object.assign(state.engine, st);
    } catch (_) {}
    renderEngine();
  }

  async function ensureEngine() {
    if (!Backend.isElectron) { toast('The jcode engine runs inside the installed desktop app.'); return; }
    if (state.engine.busy) return;
    state.engine.busy = true;
    state.engine.progress = { phase: 'meta', pct: 0 };
    renderEngine();
    const r = await Backend.jcodeEnsure();
    state.engine.busy = false;
    if (r.ok) {
      state.engine.found = true;
      state.engine.path = r.path;
      state.engine.version = r.version || null;
      state.engine.downloaded = r.downloaded;
      toast(r.downloaded ? 'jcode engine downloaded & verified ✓' : 'jcode engine ready ✓');
    } else {
      toast('Could not fetch jcode engine: ' + (r.error || 'unknown error'));
    }
    renderEngine();
  }

  /* ==================== SESSIONS ==================== */
  function renderSessions() {
    $('#session-count').textContent = state.sessions.length;
    const list = $('#session-list');
    list.innerHTML = state.sessions.map((s) => `
      <div class="session-item${s.id === state.activeId ? ' active' : ''}" data-id="${s.id}">
        <span class="s-dot"></span>
        <span class="s-name">${escapeHtml(s.name)}</span>
        <span class="s-close" data-close="${s.id}" title="Close">✕</span>
      </div>`).join('');
    renderTabs();
  }

  function renderTabs() {
    const wrap = $('#titlebar-tabs');
    wrap.innerHTML = state.sessions.map((s) => `
      <div class="tab${s.id === state.activeId ? ' active' : ''}" data-tab="${s.id}">
        <span class="tab-dot"></span>${escapeHtml(s.name)}
        <span class="tab-close" data-close="${s.id}">✕</span>
      </div>`).join('');
  }

  function persistSessions() {
    Backend.storeSaveSessions(state.sessions.map((s) => ({ id: s.id, name: s.name, cwd: s.cwd, kind: s.kind, createdAt: s.createdAt })));
  }

  async function newSession(opts) {
    opts = opts || {};
    if (!Backend.isElectron) {
      return newSessionPreview(opts);
    }
    const r = await Backend.createSession({ cwd: opts.cwd || state.settings.defaultCwd || null, args: opts.args || [], label: opts.label, cols: 110, rows: 32 });
    if (!r.ok) {
      if (r.error === 'jcode-not-found') {
        toast('Engine not installed — downloading jcode…');
        await ensureEngine();
      } else {
        toast('Failed to start session: ' + (r.error || ''));
      }
      return null;
    }
    finishSessionCreate(r.id, opts);
    return r.id;
  }

  function finishSessionCreate(id, opts) {
    const name = opts.label || opts.name || 'Session ' + (state.sessions.length + 1);
    const s = { id, name, cwd: opts.cwd || state.settings.defaultCwd || '', kind: opts.args && opts.args.length ? 'login' : 'normal', createdAt: Date.now() };
    state.sessions.push(s);
    state.activeId = id;
    TM.create(id);
    TM.activate(id);
    showTerminal();
    renderSessions();
    persistSessions();
    updateInfoPanel();
  }

  function showTerminal() {
    $('#welcome').style.display = 'none';
    $('#terminal-pane').hidden = false;
  }
  function showWelcome() {
    $('#terminal-pane').hidden = true;
    $('#welcome').style.display = '';
  }

  function activateSession(id) {
    state.activeId = id;
    TM.activate(id);
    showTerminal();
    renderSessions();
    updateInfoPanel();
  }

  function closeSession(id) {
    Backend.kill(id);
    TM.remove(id);
    state.sessions = state.sessions.filter((s) => s.id !== id);
    if (state.activeId === id) {
      state.activeId = state.sessions.length ? state.sessions[state.sessions.length - 1].id : null;
      if (state.activeId) { TM.activate(state.activeId); showTerminal(); } else showWelcome();
    }
    renderSessions();
    persistSessions();
    updateInfoPanel();
  }

  function clearActive() {
    if (state.activeId) TM.clear(state.activeId);
  }
  function stopActive() {
    if (state.activeId) Backend.write(state.activeId, '\u0003'); // Ctrl+C
  }
  function runCommand(text) {
    if (state.activeId) Backend.command(state.activeId, text);
    else toast('Start a session first');
  }
  function updateInfoPanel() {
    const s = state.sessions.find((x) => x.id === state.activeId);
    $('#ip-model').textContent = '—';
    $('#ip-provider').textContent = '—';
    $('#ip-cwd').textContent = s ? (s.cwd || '~') : '—';
    $('#ip-pid').textContent = '—';
    $('#term-cwd').textContent = s ? (s.cwd || '~/') : '~/';
    $('#term-model').textContent = s ? (s.kind === 'login' ? 'login flow' : 'model /model') : '—';
    $('#term-status-text').textContent = s ? ('session ' + s.name) : '—';
  }

  /* ==================== PROVIDER LOGIN ==================== */
  function startProviderLogin(providerId) {
    const p = PROVIDERS.find((x) => x.id === providerId);
    if (!Backend.isElectron) {
      toast(`Provider login (${p ? p.name : providerId}) runs inside the installed desktop app.`);
      return;
    }
    closeSettings();
    newSession({ label: `login · ${providerId}`, args: ['login', '--provider', providerId] });
  }

  /* ==================== COMMAND PALETTE ==================== */
  function buildCommands() {
    const c = [];
    const add = (o) => c.push(o);
    add({ id: 'new-session', icon: '✦', label: 'New Session', desc: 'Ctrl+N', run: () => newSession({}) });
    add({ id: 'open-folder', icon: '▣', label: 'Open Project Folder…', run: openFolder });
    add({ id: 'connect', icon: '◎', label: 'Connect a Provider…', run: () => { openSettings(); } });
    add({ id: 'settings', icon: '⚙', label: 'Open Settings', run: () => { openSettings(); } });
    add({ id: 'sep1', sep: true });
    add({ id: 'model', icon: '▤', label: 'Switch model', desc: '/model', run: () => runCommand('/model') });
    add({ id: 'help', icon: '?', label: 'Show jcode help', desc: '/help', run: () => runCommand('/help') });
    add({ id: 'memory', icon: '◈', label: 'Memory overview', desc: '/memory', run: () => runCommand('/memory') });
    add({ id: 'clear', icon: '⌫', label: 'Clear terminal', run: clearActive });
    add({ id: 'stop', icon: '■', label: 'Stop agent', desc: 'Ctrl+C', run: stopActive });
    add({ id: 'close-session', icon: '✕', label: 'Close current session', desc: 'Ctrl+W', run: () => state.activeId && closeSession(state.activeId) });
    add({ id: 'sep2', sep: true });
    add({ id: 'toggle-blackhole', icon: '🕳', label: 'Toggle Black Hole', run: () => toggleCosmos('blackhole') });
    add({ id: 'toggle-pulsar', icon: '✦', label: 'Toggle Pulsar Beams', run: () => toggleCosmos('pulsar') });
    add({ id: 'toggle-nebula', icon: '☁', label: 'Toggle Nebula', run: () => toggleCosmos('nebula') });
    add({ id: 'cycle-theme', icon: '◐', label: 'Cycle theme', run: cycleTheme });
    add({ id: 'toggle-panel', icon: '⇄', label: 'Toggle right panel', run: () => { state.settings.showPanel = !state.settings.showPanel; applySettings(); saveSettings(); } });
    add({ id: 'toggle-cursor', icon: '◎', label: 'Toggle custom cursor', run: () => { state.settings.customCursor = !state.settings.customCursor; applySettings(); saveSettings(); } });
    add({ id: 'sep3', sep: true });
    add({ id: 'ensure-engine', icon: '⬇', label: 'Download / verify jcode engine', run: ensureEngine });
    add({ id: 'docs', icon: '↗', label: 'jcode.sh/docs', run: () => Backend.openExternal('https://jcode.sh/docs') });
    add({ id: 'repo', icon: '↗', label: 'GitHub · 1jehuang/jcode', run: () => Backend.openExternal('https://github.com/1jehuang/jcode') });
    return c;
  }

  let paletteOpen = false;
  let paletteItems = [];
  function openPalette() {
    paletteOpen = true;
    $('#palette-overlay').hidden = false;
    $('#palette-input').value = '';
    renderPalette('');
    setTimeout(() => $('#palette-input').focus(), 30);
  }
  function closePalette() {
    paletteOpen = false;
    $('#palette-overlay').hidden = true;
  }
  function renderPalette(q) {
    q = (q || '').toLowerCase();
    const cmds = buildCommands();
    const filtered = cmds.filter((c) => !c.sep && (!q || c.label.toLowerCase().includes(q) || c.id.includes(q) || (c.desc || '').toLowerCase().includes(q)));
    paletteItems = filtered;
    const list = $('#palette-list');
    if (!filtered.length) { list.innerHTML = '<div class="palette-empty">No matching command</div>'; return; }
    list.innerHTML = filtered.map((c, i) =>
      `<div class="palette-item${i === 0 ? ' active' : ''}" data-i="${i}">
        <span class="p-ic">${c.icon}</span><span>${escapeHtml(c.label)}</span>
        ${c.desc ? `<span class="p-desc">${escapeHtml(c.desc)}</span>` : ''}
      </div>`).join('');
  }
  function runPaletteActive() {
    if (!paletteItems.length) return;
    const c = paletteItems[0];
    closePalette();
    setTimeout(() => c.run(), 0);
  }

  /* ==================== COSMOS CONTROLS ==================== */
  function toggleCosmos(key) {
    state.settings[key] = !state.settings[key];
    Cosmos.setOption(key, state.settings[key]);
    applySettings();
    saveSettings();
  }
  function cycleTheme() {
    const idx = THEMES.findIndex((t) => t.id === state.settings.theme);
    state.settings.theme = THEMES[(idx + 1) % THEMES.length].id;
    applySettings();
    saveSettings();
    toast('Theme → ' + THEMES.find((t) => t.id === state.settings.theme).label);
  }

  /* ==================== FOLDER ==================== */
  async function openFolder() {
    const p = await Backend.pickFolder();
    if (p) {
      state.settings.defaultCwd = p;
      saveSettings();
      newSession({ cwd: p, name: p.split(/[\\/]/).pop() });
    }
  }

  /* ==================== SETTINGS MODAL ==================== */
  function openSettings() {
    $('#settings-overlay').hidden = false;
    applySettings();
  }
  function closeSettings() {
    $('#settings-overlay').hidden = true;
  }

  /* ==================== PREVIEW (browser) SESSION ==================== */
  async function newSessionPreview(opts) {
    const r = await Backend.createSession({ cwd: opts.cwd || '~', cols: 110, rows: 32, label: opts.label });
    if (!r.ok) { toast('Preview terminal unavailable'); return null; }
    finishSessionCreate(r.id, opts);
    return r.id;
  }

  /* ==================== CUSTOM CURSOR ==================== */
  function initCursor() {
    const dot = $('#cursor-dot');
    const ring = $('#cursor-ring');
    let mx = 0, my = 0, rx = 0, ry = 0;
    window.addEventListener('mousemove', (e) => {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = `translate(${mx}px,${my}px) translate(-50%,-50%)`;
      const t = e.target;
      const interactive = t && t.closest && t.closest('button, a, input, .session-item, .tab, .swatch, .provider-btn');
      ring.classList.toggle('hovering', !!interactive);
      const overTerminal = t && t.closest && t.closest('#terminal');
      document.body.classList.toggle('over-terminal', !!overTerminal);
    });
    const loop = () => {
      rx += (mx - rx) * 0.16; ry += (my - ry) * 0.16;
      ring.style.transform = `translate(${rx}px,${ry}px) translate(-50%,-50%)`;
      requestAnimationFrame(loop);
    };
    loop();
    document.body.classList.add('custom-cursor');
  }

  /* ==================== MAGNETIC BUTTONS ==================== */
  function initMagnetic() {
    $$('.magnetic').forEach((el) => {
      el.addEventListener('mousemove', (e) => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) / (r.width / 2);
        const y = (e.clientY - r.top - r.height / 2) / (r.height / 2);
        el.style.transform = `translate(${x * 6}px, ${y * 6}px)`;
      });
      el.addEventListener('mouseleave', () => { el.style.transform = ''; });
    });
  }

  /* ==================== EVENTS ==================== */
  function bindEvents() {
    // window controls
    $('#btn-min').addEventListener('click', () => Backend.window.minimize());
    $('#btn-max').addEventListener('click', () => Backend.window.maximize());
    $('#btn-close').addEventListener('click', () => Backend.window.close());
    Backend.window.onMaximized((v) => { $('#btn-max').textContent = v ? '❐' : '□'; });
    Backend.window.isMaximized().then((v) => { $('#btn-max').textContent = v ? '❐' : '□'; });

    $('#btn-theme').addEventListener('click', cycleTheme);
    $('#btn-palette').addEventListener('click', openPalette);

    // sessions
    $('#btn-new-session').addEventListener('click', () => newSession({}));
    $('#welcome-new-session').addEventListener('click', () => newSession({}));
    $('#welcome-connect').addEventListener('click', () => { openSettings(); });
    $('#btn-open-folder').addEventListener('click', openFolder);
    $('#btn-new-tab').addEventListener('click', () => newSession({}));
    $('#btn-clear').addEventListener('click', clearActive);
    $('#btn-stop').addEventListener('click', stopActive);
    $('#btn-model').addEventListener('click', () => runCommand('/model'));
    $('#btn-settings').addEventListener('click', openSettings);
    $('#settings-close').addEventListener('click', closeSettings);
    $('#btn-ensure-engine').addEventListener('click', ensureEngine);
    $('#engine-card').addEventListener('click', ensureEngine);

    // session list + tabs (event delegation)
    $('#session-list').addEventListener('click', (e) => {
      const close = e.target.closest('[data-close]');
      if (close) { closeSession(close.dataset.close); return; }
      const item = e.target.closest('.session-item');
      if (item) activateSession(item.dataset.id);
    });
    $('#titlebar-tabs').addEventListener('click', (e) => {
      const close = e.target.closest('[data-close]');
      if (close) { closeSession(close.dataset.close); return; }
      const tab = e.target.closest('[data-tab]');
      if (tab) activateSession(tab.dataset.tab);
    });

    // palette
    $('#palette-input').addEventListener('input', (e) => renderPalette(e.target.value));
    $('#palette-input').addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closePalette();
      else if (e.key === 'Enter') runPaletteActive();
    });
    $('#palette-list').addEventListener('mousemove', (e) => {
      const item = e.target.closest('.palette-item');
      if (!item) return;
      $$('.palette-item').forEach((el) => el.classList.remove('active'));
      item.classList.add('active');
      paletteItems = [paletteItems[+item.dataset.i]];
    });
    $('#palette-list').addEventListener('click', (e) => {
      const item = e.target.closest('.palette-item');
      if (item) { paletteItems = [paletteItems[+item.dataset.i]]; runPaletteActive(); }
    });
    $('#palette-overlay').addEventListener('mousedown', (e) => { if (e.target === e.currentTarget) closePalette(); });
    $('#settings-overlay').addEventListener('mousedown', (e) => { if (e.target === e.currentTarget) closeSettings(); });

    // info panel toggles + quick commands
    $$('.ip-toggle').forEach((b) => b.addEventListener('click', () => {
      const map = { 'toggle-blackhole': 'blackhole', 'toggle-pulsar': 'pulsar', 'toggle-nebula': 'nebula' };
      const k = map[b.dataset.cmd];
      if (k) toggleCosmos(k);
    }));
    $$('.ip-cmd').forEach((b) => b.addEventListener('click', () => runCommand(b.dataset.run)));
    $('#ip-docs').addEventListener('click', (e) => { e.preventDefault(); Backend.openExternal('https://jcode.sh/docs'); });

    // cosmos sliders
    $('#star-density').addEventListener('input', (e) => {
      state.settings.starDensity = +e.target.value;
      Cosmos.setOption('starDensity', state.settings.starDensity);
      saveSettings();
    });
    $('#cosmos-intensity').addEventListener('input', (e) => {
      state.settings.cosmosIntensity = +e.target.value / 100;
      Cosmos.setOption('intensity', state.settings.cosmosIntensity);
      saveSettings();
    });

    // settings
    $('#opt-cursor').addEventListener('change', (e) => { state.settings.customCursor = e.target.checked; applySettings(); saveSettings(); });
    $('#opt-panel').addEventListener('change', (e) => { state.settings.showPanel = e.target.checked; applySettings(); saveSettings(); });
    $('#opt-fontsize').addEventListener('input', (e) => { state.settings.fontSize = +e.target.value; TM.setFontSize(+e.target.value); saveSettings(); });
    $('#theme-swatches').addEventListener('click', (e) => {
      const sw = e.target.closest('.swatch');
      if (sw) { state.settings.theme = sw.dataset.themeId; applySettings(); saveSettings(); }
    });

    // providers
    const grid = $('#provider-grid');
    grid.innerHTML = PROVIDERS.map((p) =>
      `<button class="provider-btn" data-provider="${p.id}"><span class="pv-ic">${p.icon}</span><span>${escapeHtml(p.name)}<span class="pv-sub">${escapeHtml(p.sub)}</span></span></button>`
    ).join('');
    grid.addEventListener('click', (e) => {
      const btn = e.target.closest('.provider-btn');
      if (btn) startProviderLogin(btn.dataset.provider);
    });

    // keyboard
    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); paletteOpen ? closePalette() : openPalette(); }
      else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'n') { e.preventDefault(); newSession({}); }
      else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'w') { e.preventDefault(); if (state.activeId) closeSession(state.activeId); }
      else if (e.key === 'Escape') { closePalette(); closeSettings(); }
    });

    // terminal data / exit wiring
    Backend.onData((id, data) => TM.write(id, data));
    Backend.onExit((id, code, signal) => {
      if (state.sessions.some((s) => s.id === id)) {
        if (state.sessions.find((s) => s.id === id).kind === 'login' && code === 0) {
          toast('Login complete — opening jcode…');
          newSession({});
        } else {
          toast(`Session exited (code ${code})`);
        }
        closeSession(id);
      }
    });

    Backend.onJcodeProgress((p) => {
      state.engine.progress = p;
      if (p.phase === 'done') { state.engine.busy = false; }
      renderEngine();
    });

    // resize
    let rt = 0;
    window.addEventListener('resize', () => {
      clearTimeout(rt);
      Cosmos.resize();
      rt = setTimeout(() => TM.refitActive(), 120);
    });

    // cosmos mouse
    window.addEventListener('mousemove', (e) => {
      Cosmos.opts.mouseX = e.clientX / window.innerWidth;
      Cosmos.opts.mouseY = 1 - e.clientY / window.innerHeight;
    }, { passive: true });
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  /* ==================== BOOT ==================== */
  async function boot() {
    runPreloader(() => {});
    TM.init($('#terminal'));
    Cosmos.init($('#cosmos-canvas'));
    Cosmos.setOption('intensity', state.settings.cosmosIntensity);
    initCursor();
    initMagnetic();

    // load persisted settings + sessions (metadata only; PTYs are recreated on demand)
    await loadSettings();
    try {
      const saved = await Backend.storeGetSessions();
      if (Array.isArray(saved)) {
        state.sessions = saved.filter((s) => s && s.id);
      }
    } catch (_) {}

    try {
      const info = await Backend.appInfo();
      document.body.dataset.platform = info.platform || 'web';
      if (info.platform === 'browser') { $('#btn-min').style.display = 'none'; $('#btn-max').style.display = 'none'; $('#btn-close').style.display = 'none'; }
    } catch (_) {}

    bindEvents();
    renderSessions();
    await refreshEngineState();

    // Auto-download engine on first desktop run when missing.
    if (Backend.isElectron && !state.engine.found) {
      setTimeout(() => ensureEngine(), 600);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
