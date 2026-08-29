import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

// Phase 0: relative base so the built renderer also loads from Electron's
// file:// origin, and a permissive host/allowlist so the sandbox preview
// (https://<port>-<id>.e2b.app) can reach the dev server.
export default defineConfig({
  base: './',
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    allowedHosts: true,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8751', changeOrigin: true },
      '/health': { target: 'http://127.0.0.1:8751', changeOrigin: true },
    },
  },
  preview: { host: '0.0.0.0', port: 4173, allowedHosts: true },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
  },
});
