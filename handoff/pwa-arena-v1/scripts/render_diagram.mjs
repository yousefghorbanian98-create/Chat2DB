// Documentation-only renderer. Does not install software or disable the sandbox.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const chrome = process.env.CHROME;
const cli = path.join(root, 'tooling/diagram/node_modules/@mermaid-js/mermaid-cli/src/cli.js');
if (!chrome || !path.isAbsolute(chrome) || !fs.existsSync(chrome) || !fs.statSync(chrome).isFile()) {
  console.error('BLOCKED: set CHROME to an absolute, approved Chromium executable. No browser was downloaded.');
  process.exit(2);
}
if (!fs.existsSync(cli)) {
  console.error('BLOCKED: install the pinned documentation workspace first; see HANDOFF.fa.md section 9.5.');
  process.exit(2);
}
const output = path.resolve(process.env.DIAGRAM_OUTPUT_DIR || path.join(root, '.cache/rendered-diagrams'));
if (output === path.join(root, 'diagrams')) {
  console.error('BLOCKED: keep the selected originals; render into a separate directory and review changes first.');
  process.exit(2);
}
fs.mkdirSync(output, { recursive: true });
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'mp-pwa-mermaid-'));
try {
  const config = path.join(temporary, 'puppeteer.json');
  fs.writeFileSync(config, JSON.stringify({ executablePath: chrome, headless: true, args: [] }), { mode: 0o600 });
  for (const format of ['svg', 'png']) {
    const result = spawnSync(process.execPath, [
      cli, '--input', path.join(root, 'diagrams/PWA_Finn_Loop_Flow.fa.mmd'),
      '--output', path.join(output, `PWA_Finn_Loop_Flow.fa.${format}`),
      '--width', '3600', '--height', '1800', '--backgroundColor', 'white',
      '--puppeteerConfigFile', config,
    ], { cwd: root, stdio: 'inherit', timeout: 120_000 });
    if (result.error || result.status !== 0) {
      console.error(`BLOCKED: ${format} renderer did not succeed. Do not claim a completed render.`);
      process.exitCode = result.status || 2;
      break;
    }
  }
  if (!process.exitCode) console.log(`Rendered documentation into ${output}; inspect it before replacing originals.`);
} finally {
  fs.rmSync(temporary, { recursive: true, force: true });
}
