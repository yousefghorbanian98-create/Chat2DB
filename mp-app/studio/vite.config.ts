import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config';

// Two installable PWAs out of one build:
//   index.html  -> admin/coach (Studio)
//   client.html -> athlete (Client)
// Relative base keeps the output loadable from a file:// shell as well as the
// local server; permissive host/allowlist so the sandbox preview
// (https://<port>-<id>.e2b.app) can reach the dev server.
export default defineConfig({
  base: './',
  plugins: [react()],
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        client: 'client.html',
      },
    },
  },
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
    coverage: {
      // The loop's quality gate, actually enforced: `npm run gate` now fails
      // below 80% instead of merely reporting a number.
      thresholds: { statements: 80, branches: 80, functions: 80, lines: 80 },
      // Bootstrap files, type-only modules and non-app assets have no logic to
      // exercise; counting them only dilutes the number.
      exclude: [
        'src/main.tsx',
        'src/client-main.tsx',
        'src/api/types.ts',
        'public/**',
        'electron/**',
        '**/*.d.ts',
        '**/*.test.{ts,tsx}',
        'vitest.setup.ts',
        '*.config.*',
      ],
    },
  },
});
