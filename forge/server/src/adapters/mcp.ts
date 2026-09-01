import type { AdapterStatus, McpServer } from '../types'
import type { Adapter } from './types'

/**
 * کلاینتِ MCP — رجیستریِ ۱۰ سرورِ همراهِ Godmode.
 * SOURCE: https://github.com/patrickking67/godmode (Apache-2.0)
 *
 * در این مرحله (طبق NG-1/NG-3) هیچ اتصالی برقرار نمی‌شود؛
 * فقط فهرست و وضعیت گزارش می‌شود. اتصالِ واقعی بعد از تثبیتِ هسته اضافه می‌شود.
 */

export const MCP_REGISTRY: McpServer[] = [
  { id: 'context7', name: 'Context7', category: 'Docs', what: 'مستنداتِ به‌روز و حساس‌به‌نسخه برای کتابخانه‌ها', transport: 'npx', target: '@upstash/context7-mcp' },
  { id: 'microsoft-learn', name: 'Microsoft Learn', category: 'Docs', what: 'مستندات و نمونه‌کد مایکروسافت/‏Azure', transport: 'http', target: 'https://learn.microsoft.com/api/mcp' },
  { id: 'aws-knowledge', name: 'AWS Knowledge', category: 'Docs', what: 'مستندات AWS و بررسیِ دسترسیِ منطقه‌ای', transport: 'http', target: 'https://knowledge-mcp.global.api.aws' },
  { id: 'cloudflare-docs', name: 'Cloudflare Docs', category: 'Docs', what: 'مستندات پلتفرمِ توسعه‌دهندگان Cloudflare', transport: 'http', target: 'https://docs.mcp.cloudflare.com/mcp' },
  { id: 'keeper-docs', name: 'Keeper Docs', category: 'Docs', what: 'مستندات Keeper Security', transport: 'http', target: 'https://docs.keeper.io/~gitbook/mcp' },
  { id: 'deepwiki', name: 'DeepWiki', category: 'Code intelligence', what: 'پرسش دربارهٔ معماری هر ریپوی عمومی', transport: 'http', target: 'https://mcp.deepwiki.com/mcp' },
  { id: 'grep-app', name: 'grep.app', category: 'Code intelligence', what: 'جستجوی regex در میلیون‌ها ریپو', transport: 'http', target: 'https://mcp.grep.app' },
  { id: 'playwright', name: 'Playwright', category: 'Browser', what: 'رانندگیِ مرورگر برای تست و اسکرین‌شات', transport: 'npx', target: '@playwright/mcp@latest' },
  { id: 'chrome-devtools', name: 'Chrome DevTools', category: 'Browser', what: 'بررسی DOM، شبکه، کنسول و عملکرد', transport: 'npx', target: 'chrome-devtools-mcp@latest' },
  { id: 'azure', name: 'Azure', category: 'Cloud', what: 'مدیریت منابع Azure (با az login محلی)', transport: 'npx', target: '@azure/mcp@latest' },
]

export class McpClient implements Adapter {
  readonly name = 'mcp'
  private enabled = new Set<string>()

  constructor(initialEnabled: string[] = []) {
    for (const id of initialEnabled) this.enabled.add(id)
  }

  list(): Array<McpServer & { enabled: boolean }> {
    return MCP_REGISTRY.map((s) => ({ ...s, enabled: this.enabled.has(s.id) }))
  }

  setEnabled(id: string, on: boolean): boolean {
    if (!MCP_REGISTRY.some((s) => s.id === id)) return false
    if (on) this.enabled.add(id)
    else this.enabled.delete(id)
    return true
  }

  async health(): Promise<AdapterStatus> {
    return {
      name: this.name,
      state: 'degraded',
      detail:
        this.enabled.size > 0
          ? `${this.enabled.size} سرور فعال انتخاب شده · اتصالِ واقعی هنوز پیاده نشده`
          : `${MCP_REGISTRY.length} سرور شناخته‌شده · هیچ‌کدام فعال نیست · اتصالِ واقعی هنوز پیاده نشده`,
    }
  }
}
