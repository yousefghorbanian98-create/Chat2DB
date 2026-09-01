// نقطهٔ ورودِ تست — قطعاتِ داخلی را برای تست‌های واحد صادر می‌کند.
// (خروجیِ اصلی برنامه dist/index.js است؛ این فایل فقط برای تست باندل می‌شود)
export { SkillRouter, tokenize } from './adapters/router'
export { SoupAdapter } from './adapters/soup'
export { JcodeAdapter } from './adapters/jcode'
export { GodmodeAdapter } from './adapters/godmode'
export { McpClient, MCP_REGISTRY } from './adapters/mcp'
export { Pipeline } from './core/pipeline'
export { Store } from './core/store'
export { buildSkills } from './core/skills'
export { config } from './config'
export {
  buildManifest,
  scanDir,
  diffManifests,
  readManifest,
  writeManifest,
  applyPack,
  untarGz,
  createTarGz,
  hashBuffer,
  totalBytes,
} from './update'
