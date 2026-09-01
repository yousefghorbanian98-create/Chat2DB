import { createServer } from 'node:http'
import { config } from './config'
import { createContext } from './context'
import { handleApi, serveStatic } from './routes'

async function main(): Promise<void> {
  const ctx = await createContext()

  const server = createServer((req, res) => {
    handleApi(req, res, ctx)
      .then((handled) => {
        // هر مسیری که API نبود → فایل‌های رابط (تک-مبدأ)
        if (!handled) return serveStatic(req, res)
        return undefined
      })
      .catch((err: unknown) => {
        // قانونِ حاکم: هیچ خطایی نباید روند را بترکاند
        const message = err instanceof Error ? err.message : 'خطای ناشناخته'
        res.writeHead(500, { 'content-type': 'application/json; charset=utf-8' })
        res.end(JSON.stringify({ error: 'internal', message }))
      })
  })

  server.listen(config.port, config.host, () => {
    // خروجی انگلیسی تا در لاگ‌های CI و ویندوز به‌هم نریزد
    console.log(`Forge server → http://${config.host}:${config.port}`)
    console.log(`skills dir: ${config.skillsDir}`)
    console.log(`web dir:    ${config.webDir ?? '(none)'}`)
    console.log(`data dir:   ${config.dataDir}`)
  })
}

main().catch((err: unknown) => {
  console.error('forge server failed to start:', err)
  process.exit(1)
})
