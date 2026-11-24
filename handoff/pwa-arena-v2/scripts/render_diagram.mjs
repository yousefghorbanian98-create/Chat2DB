#!/usr/bin/env node
// Documentation-only. Dependencies live exclusively in tooling/diagram.
import { lstat, readFile, realpath, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { dirname, extname, isAbsolute, relative, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const diagramRoot = await realpath(resolve(root, 'diagrams'));
const requireTool = createRequire(resolve(root, 'tooling/diagram/package.json'));
const [inputArg, outputArg, widthArg = '4200'] = process.argv.slice(2);
if (!inputArg || !outputArg) {
  console.error('Usage (from handoff root): node scripts/render_diagram.mjs diagrams/input.dot diagrams/output.png [1200..8000]');
  process.exit(2);
}
const input = resolve(inputArg);
const output = resolve(outputArg);
const width = Number(widthArg);
if (extname(input) !== '.dot' || extname(output) !== '.png' || !Number.isInteger(width) || width < 1200 || width > 8000) {
  throw new Error('Expected .dot input, .png output and an integer width between 1200 and 8000');
}
function inside(path) {
  const rel = relative(diagramRoot, path);
  return rel !== '' && !rel.startsWith('..') && !isAbsolute(rel);
}
async function safePath(path, mustExist) {
  if (!inside(path) || !inside(resolve(path, '..', 'sentinel'))) {
    throw new Error('Only the handoff diagrams directory is allowed');
  }
  let current = path;
  while (current !== diagramRoot) {
    try {
      if ((await lstat(current)).isSymbolicLink()) throw new Error('Symlinks are not allowed in diagram paths');
    } catch (error) {
      if (error.code !== 'ENOENT' || (current === path && mustExist)) throw error;
    }
    current = dirname(current);
  }
  if (await realpath(dirname(path)) !== dirname(path)) throw new Error('Non-canonical diagram directory');
}
const svgOutput = output.slice(0, -4) + '.svg';
await safePath(input, true);
await safePath(output, false);
await safePath(svgOutput, false);
const { instance } = await import(pathToFileURL(requireTool.resolve('@viz-js/viz')).href);
const sharp = requireTool('sharp');
const dot = await readFile(input, 'utf8');
const viz = await instance();
// Give mixed Persian/Latin labels an explicit RTL base direction. Graphviz
// positions remain unchanged; SVG/librsvg handle shaping with the local font.
const svg = viz.renderString(dot, { engine: 'dot', format: 'svg' }).replace(
  /(<text\b[^>]*)(>)([\s\S]*?)(<\/text>)/g,
  (all, attributes, close, text, end) => /[\u0600-\u06ff]/.test(text)
    ? `${attributes} direction="rtl" unicode-bidi="embed"${close}${text}${end}`
    : all,
);
await writeFile(svgOutput, svg, 'utf8');
const image = await sharp(Buffer.from(svg), { density: 72 })
  .resize({ width })
  .png({ compressionLevel: 9, adaptiveFiltering: true })
  .toFile(output);
console.log(JSON.stringify({ input, svg: svgOutput, png: output, width: image.width, height: image.height, bytes: image.size, graphviz: viz.graphvizVersion, sharp: sharp.versions.sharp, status: 'DIAGRAM_ONLY_NOT_PRODUCT_QA' }));
