'use strict';
/**
 * TerminalManager — one xterm.js instance per session so each session keeps its
 * own live TUI screen. Handles fit, resize, web-links and WebGL rendering.
 */
(function () {
  const manager = {
    instances: new Map(), // id -> { term, fit, addon, container }
    activeId: null,
    container: null,
    fontSize: 14,
    fontFamily: "'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace",

    init(container) {
      this.container = container;
    },

    theme() {
      return {
        background: 'rgba(0,0,0,0)',
        foreground: '#e6e6f0',
        cursor: '#8b5cf6',
        cursorAccent: '#000000',
        selectionBackground: 'rgba(139,92,246,0.35)',
        black: '#0a0a1a', red: '#f87171', green: '#10b981', yellow: '#fbbf24',
        blue: '#60a5fa', magenta: '#a78bfa', cyan: '#06b6d4', white: '#e6e6f0',
        brightBlack: '#606080', brightRed: '#fca5a5', brightGreen: '#6ee7b7',
        brightYellow: '#fde68a', brightBlue: '#93c5fd', brightMagenta: '#c4b5fd',
        brightCyan: '#67e8f9', brightWhite: '#ffffff'
      };
    },

    create(id) {
      if (this.instances.has(id)) return this.instances.get(id).term;
      const term = new window.Terminal({
        fontFamily: this.fontFamily,
        fontSize: this.fontSize,
        cursorBlink: true,
        cursorStyle: 'block',
        scrollback: 8000,
        allowTransparency: true,
        theme: this.theme(),
        letterSpacing: 0.3,
        lineHeight: 1.2
      });
      const fit = new window.FitAddon.FitAddon();
      const links = new window.WebLinksAddon.WebLinksAddon();
      term.loadAddon(fit);
      term.loadAddon(links);
      try {
        term.loadAddon(new window.WebglAddon.WebglAddon());
      } catch (_) { /* WebGL renderer optional */ }

      const container = document.createElement('div');
      container.className = 'xterm-host';
      container.style.cssText = 'position:absolute;inset:0;display:block;';
      this.container.appendChild(container);
      term.open(container);
      term.element.style.padding = '4px 2px';

      term.onData((data) => window.Backend.write(id, data));

      this.instances.set(id, { term, fit, container });
      return term;
    },

    activate(id) {
      for (const [sid, inst] of this.instances) {
        inst.container.style.display = sid === id ? 'block' : 'none';
      }
      this.activeId = id;
      this._refit(id);
      const inst = this.instances.get(id);
      if (inst) inst.term.focus();
    },

    refitActive() {
      if (this.activeId) this._refit(this.activeId);
    },

    _refit(id) {
      const inst = this.instances.get(id);
      if (!inst) return;
      try { inst.fit.fit(); } catch (_) {}
      const dims = inst.term.rows && inst.term.cols ? { cols: inst.term.cols, rows: inst.term.rows } : null;
      if (dims) window.Backend.resize(id, dims.cols, dims.rows);
    },

    setFontSize(px) {
      this.fontSize = px;
      for (const inst of this.instances.values()) {
        inst.term.options.fontSize = px;
        try { inst.fit.fit(); } catch (_) {}
      }
    },

    write(id, data) {
      const inst = this.instances.get(id);
      if (inst) inst.term.write(data);
    },

    clear(id) {
      const inst = this.instances.get(id);
      if (inst) inst.term.clear();
    },

    remove(id) {
      const inst = this.instances.get(id);
      if (inst) {
        try { inst.term.dispose(); } catch (_) {}
        if (inst.container.parentNode) inst.container.parentNode.removeChild(inst.container);
        this.instances.delete(id);
      }
      if (this.activeId === id) this.activeId = null;
    },

    removeAll() {
      for (const id of [...this.instances.keys()]) this.remove(id);
    }
  };

  window.TerminalManager = manager;
})();
