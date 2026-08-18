import { copyFileSync, existsSync, mkdirSync } from 'node:fs'
import { spawnSync } from 'node:child_process'
import path from 'node:path'

if (process.platform !== 'win32') {
  throw new Error('The release sidecar must be built on Windows x64')
}

const python = process.env.EASYCLIP_PYTHON || 'python'
const engine = path.resolve('resources/engine')
const result = spawnSync(python, ['-m', 'PyInstaller', '--noconfirm', 'easyclip-engine.spec'], {
  cwd: engine,
  stdio: 'inherit'
})
if (result.error) throw result.error
if (result.status !== 0) throw new Error(`PyInstaller exited with code ${String(result.status)}`)

const source = path.join(engine, 'dist', 'easyclip-engine.exe')
if (!existsSync(source)) throw new Error(`PyInstaller did not create ${source}`)
const destination = path.resolve('resources/binaries/easyclip-engine.exe')
mkdirSync(path.dirname(destination), { recursive: true })
copyFileSync(source, destination)
console.log(`Local AI engine copied to ${destination}`)
