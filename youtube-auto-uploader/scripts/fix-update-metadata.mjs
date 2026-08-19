import { readFileSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const packageJson = JSON.parse(readFileSync(path.resolve('package.json'), 'utf8'))
const metadata = path.resolve('dist/latest.yml')
const generated = `YouTube-Auto-Uploader-${packageJson.version}-x64.exe`
const released = `YouTube.Auto-Uploader.${packageJson.version}.x64.exe`
const content = readFileSync(metadata, 'utf8')
if (!content.includes(generated)) throw new Error(`Update metadata does not reference expected installer: ${generated}`)
writeFileSync(metadata, content.replaceAll(generated, released), 'utf8')
console.log(`Update metadata normalized for GitHub release asset: ${released}`)
