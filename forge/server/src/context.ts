import { SoupAdapter } from './adapters/soup'
import { JcodeAdapter } from './adapters/jcode'
import { GodmodeAdapter } from './adapters/godmode'
import { McpClient } from './adapters/mcp'
import { Store } from './core/store'
import { Pipeline } from './core/pipeline'
import { buildSkills } from './core/skills'
import type { Adapter } from './adapters/types'

export interface AppContext {
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

  const jcode = new JcodeAdapter()
  const mcp = new McpClient()
  const store = new Store()
  const pipeline = new Pipeline(soup, godmode, jcode)

  return { soup, jcode, godmode, mcp, store, pipeline, adapters: [jcode, soup, godmode, mcp] }
}
