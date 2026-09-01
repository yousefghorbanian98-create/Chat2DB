import { config } from './config'
import { SoupAdapter } from './adapters/soup'
import { JcodeAdapter } from './adapters/jcode'
import { GodmodeAdapter } from './adapters/godmode'
import { McpClient } from './adapters/mcp'
import { Store } from './core/store'
import { Pipeline } from './core/pipeline'
import { ProviderAdapter } from './adapters/provider'
import { loadSettings, patchSettings } from './core/settings'
import type { Settings } from './types'
import { buildSkills } from './core/skills'
import type { Adapter } from './adapters/types'

export interface AppContext {
  provider: ProviderAdapter
  settings: Settings
  saveSettings: (patch: Partial<Settings>) => Promise<Settings>
  soup: SoupAdapter
  jcode: JcodeAdapter
  godmode: GodmodeAdapter
  mcp: McpClient
  store: Store
  pipeline: Pipeline
  adapters: Adapter[]
}

export async function createContext(): Promise<AppContext> {
  const godmode = new GodmodeAdapter()
  await godmode.load()

  const soup = new SoupAdapter()
  soup.setSkills(buildSkills(godmode))

  // تنظیمات از دیسک — شاملِ پوشه‌ی پروژه و اتصال به مدل
  const settings = await loadSettings()

  const jcode = new JcodeAdapter(settings.jcodePath ?? config.jcodeBin)
  const provider = new ProviderAdapter(settings.provider)
  const mcp = new McpClient(settings.mcpEnabled)
  const store = new Store()

  // مقدارِ زنده: اگر کاربر تنظیمات را عوض کند، پایپ‌لاین همان را می‌خواند
  let current = settings
  const saveSettings = async (patch: Partial<Settings>) => {
    current = await patchSettings(patch)
    provider.setConfig(current.provider)
    jcode.setBinary(current.jcodePath ?? config.jcodeBin)
    for (const id of current.mcpEnabled) mcp.setEnabled(id, true)
    return current
  }

  const pipeline = new Pipeline(soup, godmode, jcode, provider, () => current)

  return {
    soup,
    jcode,
    godmode,
    mcp,
    store,
    pipeline,
    provider,
    settings: current,
    saveSettings,
    adapters: [provider, jcode, soup, godmode, mcp],
  }
}
