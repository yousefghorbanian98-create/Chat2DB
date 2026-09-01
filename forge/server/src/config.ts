import { existsSync } from 'node:fs'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))

/** اولین مسیر موجود را از میان نامزدها برمی‌گرداند. */
function firstExisting(candidates: string[]): string | null {
  for (const c of candidates) {
    try {
      if (existsSync(c)) return c
    } catch {
      // مسیر نامعتبر را نادیده بگیر
    }
  }
  return null
}

function resolveSkillsDir(): string {
  const fromEnv = process.env.FORGE_SKILLS_DIR
  if (fromEnv) return resolve(fromEnv)
  // dist/ یا src/ → ../../skills  (حالت توسعه)
  // resources/server → ../skills  (حالت بسته‌بندی‌شده در Tauri)
  return (
    firstExisting([
      resolve(here, './skills'), // بسته‌بندی‌شده: resources/server/skills
      resolve(here, '../../skills'), // توسعه: forge/skills
      resolve(here, '../skills'),
      resolve(here, '../../../skills'),
    ]) ?? resolve(here, './skills')
  )
}

/**
 * پوشه‌ی رابطِ کاربریِ ساخته‌شده.
 * اگر وجود داشته باشد، سرور آن را هم سرو می‌کند (تک-مبدأ — single origin).
 * این کار باعث می‌شود در برنامه‌ی بسته‌بندی‌شده نیازی به فراخوانیِ
 * localhost از سوی مرورگر نباشد و همان مسیرهای نسبیِ /api کار کنند.
 */
function resolveWebDir(): string | null {
  const fromEnv = process.env.FORGE_WEB_DIR
  if (fromEnv) return resolve(fromEnv)
  // dist/ یا src/ → ../web  (در بسته‌بندی: resources/server/web)
  // حالت توسعه:            ../../dist (خروجیِ vite)
  return firstExisting([resolve(here, '../web'), resolve(here, '../../dist')])
}

function resolveDataDir(): string {
  const fromEnv = process.env.FORGE_DATA_DIR
  if (fromEnv) return resolve(fromEnv)
  return resolve(here, '../../.data')
}

export const config = {
  port: Number(process.env.FORGE_PORT ?? 8787),
  host: process.env.FORGE_HOST ?? '127.0.0.1',
  skillsDir: resolveSkillsDir(),
  webDir: resolveWebDir(),
  dataDir: resolveDataDir(),
  /** باینری jcode — قابل تنظیم برای نصب‌های غیر استاندارد */
  jcodeBin: process.env.FORGE_JCODE_BIN ?? 'jcode',
  /** مفسر پایتون برای Soup پایتونی (اختیاری) */
  pythonBin: process.env.FORGE_PYTHON_BIN ?? (process.platform === 'win32' ? 'python' : 'python3'),
  /** سقف تعداد skill تزریق‌شده در هر فراخوانی */
  maxSkillsPerCall: Number(process.env.FORGE_MAX_SKILLS ?? 3),
} as const
